import numbers as _numbers
import numpy as _np
from pyg4ometry.gdml import Units as _Units


class BasicExpression:
    """
    Holds an expression as a string and can use the expression parser
    in the supplied registry to evaluate it. A registry is required.

    :param name: Name of the expression object
    :type name: str
    :param expressionString: Expression itself as a string e.g. "12.0" or "a + 3.0"
    :type expressionString: str
    :param registry: The registry object to give context for any variables used.
    :type registry: pyg4ometry.geant4.Registry.Registry

    >>> r = pyg4ometry.geant4.Registry()
    >>> a = BasicExpression("a", "3.0", r)
    >>> float(a)
    >>> str(a)
    """
    def __init__(self, name, expressionString, registry):
        self.name = name
        self.expressionString = expressionString
        self.parseTree = None
        self.registry = registry

    def eval(self):
        expressionParser = self.registry.getExpressionParser()
        self.parseTree = expressionParser.parse(self.expressionString)
        value = expressionParser.evaluate(self.parseTree, self.registry.defineDict)
        return value

    def variables(self, allDependents=False):
        expressionParser = self.registry.getExpressionParser()
        self.parseTree = expressionParser.parse(self.expressionString)
        variables = expressionParser.get_variables(self.parseTree)
        if allDependents:
            dependents = []
            for v in variables:
                if v in self.registry.defineDict:
                    define = self.registry.defineDict[v]
                    dependents = define.expression.variables() + dependents # prepend
            variables = dependents + variables # prepend
        result = []
        [result.append(v) for v in variables if v not in result] # remove duplicates but preserve prepended order
        return result

    def simp(self):
        # find all variables of the expression and create
        pass

    def __repr__(self):
        return "{} : {}".format(self.name, self.expressionString)

    def __float__(self):
        return self.eval()

    def str(self):
        return 'BasicExpression : '+self.name+' : '+str(float(self))


def upgradeToStringExpression(reg, obj):
    """
    Take a float, str, ScalarBase and return string expression.

    :param reg: Registry for lookup in define dictionary
    :type reg: Registry
    :param obj: Object to upgrade
    :type obj: str,float,ScalarBase
    :return: String expression
    :rtype: str
    """
    if isinstance(obj, _numbers.Number):
        # return str(obj)                  # number like so return string
        return "%.15f" % obj

    elif isinstance(obj, str):# or isinstance(obj,unicode) :
        if obj in reg.defineDict:  # not sure if this is needed
            return obj
        else :
            e = BasicExpression("", obj, reg)
            try:
                e.eval()
                return obj
            except Exception as err:
                msg = "<= Cannot evaluate expression : {}".format(obj)
                if not err.args:
                    err.args=('',)
                err.args = err.args + (msg,)
                raise

    elif isinstance(obj, ScalarBase):
        if obj.name in reg.defineDict:
            return obj.name             # so a scalar expression in registry
        else:
            return obj.expression.expressionString  # so a scalar expression not in registry

    else:
        raise ValueError("upgradeToStringExpression> unsupported type ("+str(type(obj))+")")

def evaluateToFloat(reg, obj):
    try:
        if isinstance(obj, str):
            raise AttributeError
        ans = [evaluateToFloat(reg, item) for item in obj.__iter__()]
    except (AttributeError, ):
        if isinstance(obj, _numbers.Number) or isinstance(obj, BasicExpression):
            return float(obj)
        elif isinstance(obj, ScalarBase) or isinstance(obj, VectorBase):
            return obj.eval()
        else:
            evaluatable = BasicExpression("",obj,reg)
        ans = float(evaluatable.eval())
    return ans

def upgradeToExpression(reg, obj):
    """
    Helper functions that takes a string and returns an expression object or a string
    """

    # TODO: consider merging into/reusing the upgradeToStringExpression
    as_string  = upgradeToStringExpression(reg, obj)
    expression = BasicExpression("" ,as_string, reg)

    try:
        float(expression)
        return expression
    except ValueError:
        return as_string

def upgradeToVector(var, reg, type="position", unit="", addRegistry=False):
    """
    Take a list [x,y,z] and create a vector 

    :param var: input list to create a position, rotation or scale
    :type var: list of str, float, Constant, Quantity, Variable
    :param reg: registry
    :type reg: Registry
    :param type: class type of vector (position, rotation, scale)
    :type type: str
    :param addRegistry: flag to add to registry
    :type addRegistry: bool
    """
    # check units
    if type == "position" and unit == "":
        unit = "mm"
    elif type == "rotation" and unit == "":
        unit = "rad"

    # check if already a vector type 
    if isinstance(var, VectorBase):
        return var 

    # create appropriate vector type
    if isinstance(var,list) or isinstance(var,_np.ndarray):
        if type == "position":
            return Position("",var[0],var[1],var[2],unit,reg, addRegistry)
        elif type == "rotation":
            return Rotation("",var[0],var[1],var[2],unit,reg, addRegistry)
        elif type == "scale":
            return Scale("",var[0],var[1],var[2],"none",reg, addRegistry)
        else : 
            print('type not defined')

def upgradeToTransformation(var, reg, addRegistry=False):
    """
    Take a list of lists [[rx,ry,rz],[x,y,z]] and create a transformation [Rotation,Position]

    :param var: input list to create a transformation
    :type var: list of str, float, Constant, Quantity, Variable
    :param reg: registry
    :type reg: Registry
    :param addRegistry: flag to add to registry
    :type addRegistry: bool
    """
    if isinstance(var[0],VectorBase):
        rot = var[0]
    elif isinstance(var[0],list):
        try:
            aunit = var[0][3]
        except:
            aunit = ""
        rot = upgradeToVector(var[0],reg,"rotation",aunit,addRegistry)
    else:
        raise TypeError("Unknown rotation type: {}".format(type(var[0])))

    if isinstance(var[1],VectorBase):
        tra = var[1]
    elif isinstance(var[1],list):
        try:
            lunit = var[1][3]
        except:
            lunit = ""
        tra = upgradeToVector(var[1],reg,"position",lunit,addRegistry)
    else:
        raise TypeError("Unknown position type: {}".format(type(var[1])))


    return [rot,tra]

class DefineBase:
    """
    Common bits for a define. Must have a name and a registry. Adding
    to the registry can't be done here as it must be done by the derived type.
    """
    def __init__(self, name="", registry=None):
        self.name = name
        self.registry = registry

    def setName(self, name):
        """
        Set name of the object.

        :param name: name of object
        :type name: str
        """
        self.name = name

    def setRegistry(self, registry):
        self.registry = registry

class ScalarBase(DefineBase):
    """
    Base class for all scalars (Constants, Quantity, Variable and 'Expression')
    """
    def __init__(self, typeName, name="", registry=None):
        super(ScalarBase, self).__init__(name, registry)
        self.expression = None
        self._typeName = typeName

    def setName(self, name):
        """
        Set name of scalar

        :param name: name of object
        :type name: str
        """
        super().setName(name)
        self.expression.name = 'expr_{}'.format(name)

    def setExpression(self, expressionString):
        """
        Take a string and make it into the BasicExpression type for this object.

        :param expressionString: Expression to store.
        :type expressionString: str
        """
        self.expression = BasicExpression('expr_{}'.format(self.name), upgradeToStringExpression(self.registry, expressionString), self.registry)

    def setRegistry(self, registry):
        super().setRegistry(registry)
        if self.expression:
            registry.transferDefine(self)

    def eval(self):
        """
        Evaluate the expression

        :return: numerical evaluation of Constant
        :rtype: float
        """
        return self.expression.eval()

    def __repr__(self):
        return self._typeName + " : {} = {}".format(self.name, str(self.expression))

    def __float__(self):
        return self.expression.eval()

    def __add__(self, other):
        v1 = upgradeToStringExpression(self.registry,self)
        v2 = upgradeToStringExpression(self.registry,other)

        v = Constant("var_{}_add_{}".format(v1,v2), '({}) + ({})'.format(v1, v2),
                     registry=self.registry,
                     addRegistry=False)
        return v

    def __sub__(self, other):
        v1 = upgradeToStringExpression(self.registry,self)
        v2 = upgradeToStringExpression(self.registry,other)

        v = Constant("var_{}_sub_{}".format(v1,v2), '({}) - ({})'.format(v1, v2),
                     registry=self.registry,
                     addRegistry=False)
        return v

    def __rsub__(self,other) :
        v1 = upgradeToStringExpression(self.registry,self)
        v2 = upgradeToStringExpression(self.registry,other)        
        
        v = Constant("var_{}_sub_{}".format(v2,v1), '({}) - ({})'.format(v2, v1),
                     registry=self.registry,
                     addRegistry=False)
        return v        

    def __mul__(self, other):
        # check to see if other is a vector 
        if isinstance(other,VectorBase) : 
            return other*self

        v1 = upgradeToStringExpression(self.registry,self)
        v2 = upgradeToStringExpression(self.registry,other)

        v = Constant("var_{}_mul_{}".format(v1,v2), '({}) * ({})'.format(v1, v2),
                     registry=self.registry,
                     addRegistry=False)
        return v

    def __truediv__(self, other):
        v1 = upgradeToStringExpression(self.registry,self)
        v2 = upgradeToStringExpression(self.registry,other)

        v = Constant("var_{}_div_{}".format(v1,v2), '({}) / ({})'.format(v1, v2),
                     registry=self.registry,
                     addRegistry=False)
        return v

    def __rtruediv__(self, other):
        v1 = upgradeToStringExpression(self.registry,self)
        v2 = upgradeToStringExpression(self.registry,other)

        v = Constant("var_{}_div_{}".format(v2,v1), '({}) / ({})'.format(v2, v1),
                     registry=self.registry,
                     addRegistry=False)
        return v

    def __neg__(self):
        v1 = upgradeToStringExpression(self.registry,self)

        v = Constant("var_neg_{}".format(v1), '-({})'.format(v1),
                     registry=self.registry,
                     addRegistry=False)
        return v

    def __abs__(self):
        return abs(self)

    def __pow__(self, power):
        return pow(self,power)

    __radd__ = __add__
    __rmul__ = __mul__

def sin(arg):
    """
    Sin of a ScalarBase object, returns a Constant
    
    :param arg: Argument of sin
    :type  arg: Constant, Quantity, Variable or Expression
    """

    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("sin_{}".format(v1), 'sin({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v

def cos(arg):
    """
    Cosine of a ScalarBase object, returns a Constant
    
    :param arg: Argument of cos
    :type  arg: Constant, Quantity, Variable or Expression
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("cos_{}".format(v1), 'cos({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v

def tan(arg):
    """
    Tangent of a ScalarBase object, returns a Constant
    
    :param arg: Argument of tan
    :type  arg: Constant, Quantity, Variable or Expression
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("tan_{}".format(v1), 'tan({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v

def asin(arg):
    """
    ArcSin of a ScalarBase object, returns a Constant
    
    :param arg: Argument of asin
    :type  arg: Constant, Quantity, Variable or Expression
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("sin_{}".format(v1), 'asin({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v

def acos(arg):
    """
    ArcCos of a ScalarBase object, returns a Constant
    
    :param arg: Argument of acos
    :type  arg: Constant, Quantity, Variable or Expression
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("cos_{}".format(v1), 'acos({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v

def atan(arg):
    """
    ArcTan of a ScalarBase object, returns a Constant
    
    :param arg: Argument of tan
    :type  arg: Constant, Quantity, Variable or Expression
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("tan_{}".format(v1), 'atan({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v

def exp(arg):
    """
    Exponential of a ScalarBase object, returns a Constant
    
    :param arg: Argument of exp
    :type  arg: Constant, Quantity, Variable or Expression
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("exp_{}".format(v1), 'exp({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v

def log(arg):
    """
    Natural logarithm of a ScalarBase object, returns a Constant
    
    :param arg: Argument of log
    :type  arg: Constant, Quantity, Variable or Expression
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("log_{}".format(v1), 'log({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v

def log10(arg):
    """
    Base 10 logarithm of a ScalarBase object, returns a Constant
    
    :param arg: Argument of log10
    :type  arg: Constant, Quantity, Variable or Expression
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("log10_{}".format(v1), 'log10({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v

def sqrt(arg):
    """
    Square root of a ScalarBase object, returns a Constant
    
    :param arg: Argument of sin
    :type  arg: Constant, Quantity, Variable or Expression
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("sqrt_{}".format(v1), 'sqrt({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v    

def pow(arg, power):
    """
    arg raised to power 
    
    :param arg: Argument of x**y
    :type  arg: Constant, Quantity, Variable or Expression
    :param power: y 
    :type power: float
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("sqrt_{}".format(v1), 'pow({},{})'.format(v1,str(power)),registry=arg.registry, addRegistry=False)        
    return v

def abs(arg):
    """
    absolute value of arg

    :param arg: Argument of abs(arg)
    :type  arg: Constant, Quantity, Variable or Expression
    """
    v1 = upgradeToStringExpression(arg.registry,arg)
    v = Constant("abs_{}".format(v1), 'abs({})'.format(v1),registry=arg.registry, addRegistry=False)
    return v


class Constant(ScalarBase):
    """
    GDML constant define wrapper object
    
    :param name: of constant for registry
    :type name: str
    :param value: expression for constant
    :type value: float,str,Constant,Quantity,Variable
    :param registry: for storing define
    :type registry: Registry
    :param addRegistry: add constant to registry
    :type addRegistry: bool
    """
    def __init__(self, name, value, registry, addRegistry=True):
        super(Constant, self).__init__("Constant", name, registry)
        self.expression = BasicExpression("expr_{}".format(name), upgradeToStringExpression(registry,value),registry)

        if registry and addRegistry:
            registry.addDefine(self)

    def __eq__(self, other):
        if isinstance(other, Constant):
            return self.eval() == other.eval()
        else:
            return self.eval() == other

    def __ne__(self, other):
        if isinstance(other, Constant):
            return self.eval() != other.eval()
        else:
            return self.eval() != other

    def __lt__(self, other):
        if isinstance(other, Constant):
            return self.eval() < other.eval()
        else:
            return self.eval() < other

    def __gt__(self, other):
        if isinstance(other, Constant):
            return self.eval() > other.eval()
        else:
            return self.eval() > other

    def __le__(self, other):
        if isinstance(other, Constant):
            return self.eval() <= other.eval()
        else:
            return self.eval() <= other

    def __ge__(self, other):
        if isinstance(other, Constant):
            return self.eval() >= other.eval()
        else:
            return self.eval() >= other


class Quantity(ScalarBase):
    """
    GDML quantity define wrapper object
    
    :param name: of constant for registry
    :type name: str
    :param value: expression for constant
    :type value: float,str,Constant,Quantity,Variable
    :param unit: unit of the quantity 
    :type unit: str
    :param type: type of quantity
    :type type: not sure
    :param registry: for storing define
    :type registry: Registry
    :param addRegistry: add constant to registry
    :type addRegistry: bool
    """
    def __init__(self, name, value, unit, type, registry, addRegistry=True):
        super(Quantity, self).__init__("Quantity", name, registry)
        self.unit = unit
        self.type = type
        self.expression = BasicExpression("expr_{}".format(name), upgradeToStringExpression(registry, value), registry)

        if registry and addRegistry:
            registry.addDefine(self)

    def __repr__(self):
        return self._typeName + " : {} = {} [{}] {}".format(self.name, str(self.expression), self.unit, self.type)


class Variable(ScalarBase):
    """
    GDML variable define wrapper object
    
    :param name: of constant for registry
    :type name: str
    :param value: expression for constant
    :type value: float,str,Constant,Quantity,Variable
    :param registry: for storing define
    :type registry: Registry
    """
    def __init__(self, name, value, registry, addRegistry=True):
        super(Variable, self).__init__("Variable", name, registry)
        self.expression = BasicExpression("expr_{}".format(name), upgradeToStringExpression(registry,value),registry)

        if registry and addRegistry:
            registry.addDefine(self)

class Expression(ScalarBase):
    """
    General expression, does not have an analogue in GDML
    
    :param name: of constant for registry
    :type name: str
    :param value: expression for constant
    :type value: float,str,Constant,Quantity,Variable
    :param registry: for storing define
    :type registry: Registry
    :param addRegistry: add constant to registry
    :type addRegistry: bool
    """
    def __init__(self, name, value, registry, addRegistry=False):
        super(Expression, self).__init__("Expression", name, registry)
        self.expression = BasicExpression("expr_{}".format(name), upgradeToStringExpression(registry,value),registry)

        if registry and addRegistry:
            registry.addDefine(self)

    def __int__(self):
        return int(self.expression.eval())


class VectorBase:
    def __init__(self, typeName, name, registry):
        self._typeName = typeName
        self.name = name
        self.registry = registry
        self.x = None
        self.y = None
        self.z = None
        self.unit = None

    def __repr__(self):
        return self._typeName + " : {} = [{} {} {}]".format(self.name, str(self.x), str(self.y), str(self.z))
    
    def __add__(self, other):
        p  = Position("vec_{}_add_{}".format(self.name,other.name),
                      '({})+({})'.format(self.x.expressionString, other.x.expressionString),
                      '({})+({})'.format(self.y.expressionString, other.y.expressionString),
                      '({})+({})'.format(self.z.expressionString, other.z.expressionString),
                      self.unit,
                      self.registry,
                      False)
        p.registry      = self.registry
        p.x.registry    = self.registry
        p.y.registry    = self.registry
        p.z.registry    = self.registry
        return p

    def __sub__(self, other):

        other = upgradeToVector(other, self.registry, "position", "", False)

        p  = Position("vec_{}_sub_{}".format(self.name, other.name),
                      '({})-({})'.format(self.x.expressionString, other.x.expressionString),
                      '({})-({})'.format(self.y.expressionString, other.y.expressionString),
                      '({})-({})'.format(self.z.expressionString, other.z.expressionString),
                      self.unit,
                      self.registry,
                      False)
        p.registry      = self.registry
        p.x.registry    = self.registry
        p.y.registry    = self.registry
        p.z.registry    = self.registry
        return p

    def __mul__(self, other):
        #v1 = upgradeToStringExpression(self.registry, self)
        v2 = upgradeToStringExpression(self.registry, other)
        
        p = Position("vec_{}_mul_{}".format(self.name, v2),
                     '({})*({})'.format(self.x.expressionString, v2),
                     '({})*({})'.format(self.y.expressionString, v2),
                     '({})*({})'.format(self.z.expressionString, v2),
                     self.unit,
                     self.registry,
                     False)
        p.registry      = self.registry
        p.x.registry    = self.registry
        p.y.registry    = self.registry
        p.z.registry    = self.registry
        return p                     

    __rmul__ = __mul__

    def __truediv__(self, other):
        #v1 = upgradeToStringExpression(self.registry,self)
        v2 = upgradeToStringExpression(self.registry,other)
        
        p = Position("vec_{}_div_{}".format(self.name, v2),
                     '({})/({})'.format(self.x.expressionString, v2),
                     '({})/({})'.format(self.y.expressionString, v2),
                     '({})/({})'.format(self.z.expressionString, v2),
                     self.unit,
                     self.registry,
                     False)
        p.registry      = self.registry
        p.x.registry    = self.registry
        p.y.registry    = self.registry
        p.z.registry    = self.registry
        return p                     
    
    def setName(self, name):
        """
        Set name of vector

        :param name: name of object
        :type name: str
        """
        self.name          = name
        self.x.registry    = self.registry 
        self.y.registry    = self.registry 
        self.z.registry    = self.registry 
        self.x.name        = 'expr_{}_vec_x'.format(name)
        self.y.name        = 'expr_{}_vec_y'.format(name)
        self.z.name        = 'expr_{}_vec_z'.format(name)
        self.registry.addDefine(self)

    def eval(self):
        """ 
        Evaluate vector 

        :return: numerical evaluation of vector
        :rtype: list of floats
        """
        u = _Units.unit(self.unit)
        return [self.x.eval()*u, self.y.eval()*u, self.z.eval()*u]

    def nonzero(self):
        """ 
        Evaluate vector 

        :return: Check if the vector is trivial (all elements zero)
        :rtype: bool
        """
        return any(self.eval())

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y 
        elif key == 2:
            return self.z
        else:
            raise IndexError

    def setRegistry(self, registry):
        self.registry = registry
        self.x.registry    = self.registry
        self.y.registry    = self.registry
        self.z.registry    = self.registry


class Position(VectorBase):
    """
    GDML position define wrapper object
 
    :param x: x component of position 
    :type x: float, Constant, Quantity, Variable
    :param y: y component of position 
    :type y: float, Constant, Quantity, Variable
    :param z: z component of position 
    :type z: float, Constant, Quantity, Variable
    """
    def __init__(self, name, x, y, z, unit="mm", registry=None, addRegistry=True):
        super(Position, self).__init__("Position", name, registry)

        if unit is not None:
            if not isinstance(unit, str):
                raise ValueError("unit must be None or a string")
            self.unit = unit
        else:
            self.unit = "mm"

        self.x = BasicExpression("expr_pos_x_{}".format(name), upgradeToStringExpression(registry,x), registry=registry)
        self.y = BasicExpression("expr_pos_y_{}".format(name), upgradeToStringExpression(registry,y), registry=registry)
        self.z = BasicExpression("expr_pos_z_{}".format(name), upgradeToStringExpression(registry,z), registry=registry)
               
        if registry and addRegistry:
            self.registry.addDefine(self)


class Rotation(VectorBase):
    """
    GDML rotation define wrapper object
 
    :param rx: rotation around x axis
    :type rx: float, Constant, Quantity, Variable
    :param ry: rotation around y axis 
    :type ry: float, Constant, Quantity, Variable
    :param rz: rotation around z axis
    :type rz: float, Constant, Quantity, Variable
    """
    def __init__(self, name, rx, ry, rz, unit="rad", registry=None, addRegistry=True):
        super(Rotation, self).__init__("Rotation", name, registry)

        if unit is not None:
            if not isinstance(unit, str):
                raise ValueError("unit must be None or a string")
            acceptableUnits = ['rad', 'radian', 'mrad', 'milliradian', 'deg', 'degree']
            if unit not in acceptableUnits:
                raise ValueError("Invalid unit \""+unit+"\" in rotation define \""+name+"\" - can be one of:  "+", ".join(acceptableUnits))
            self.unit = unit
        else:
            self.unit = "rad"

        self.x = BasicExpression("expr_rot_x_{}".format(name), upgradeToStringExpression(registry,rx), registry=registry)
        self.y = BasicExpression("expr_rot_y_{}".format(name), upgradeToStringExpression(registry,ry), registry=registry)
        self.z = BasicExpression("expr_rot_z_{}".format(name), upgradeToStringExpression(registry,rz), registry=registry)

        if registry and addRegistry:
            self.registry.addDefine(self)


class Scale(VectorBase):
    """
    GDML scale define wrapper object
 
    :param sx: x component of scale 
    :type sx: float, Constant, Quantity, Variable
    :param sy: y component of scale
    :type sy: float, Constant, Quantity, Variable
    :param sz: z component of scale
    :type sz: float, Constant, Quantity, Variable
    """
    def __init__(self, name, sx, sy, sz, unit=None, registry=None, addRegistry=True):
        super(Scale, self).__init__("Scale", name, registry)

        if unit != None:
            if not isinstance(unit, str):
                raise ValueError("unit must be None or a string")
            self.unit = unit
        else:
            self.unit = "none"

        self.x = BasicExpression("expr_scl_x_{}".format(name), upgradeToStringExpression(registry,sx), registry=registry)
        self.y = BasicExpression("expr_scl_y_{}".format(name), upgradeToStringExpression(registry,sy), registry=registry)
        self.z = BasicExpression("expr_scl_z_{}".format(name), upgradeToStringExpression(registry,sz), registry=registry)

        if registry and addRegistry:
            self.registry.addDefine(self)


class Matrix:
    """
    GDML matrix define wrapper object
    
    :param name: of matrix for registry
    :type name: str
    :param coldim: is number of columns
    :param coldim: int
    :param values: list of values for matrix
    :type values: list of float, str, Constant, Quantity, Variable
    :param registry: for storing define
    :type registry: Registry
    :param addRegistry: add matrix to registry
    :type addRegistry: bool
    """
    def __init__(self, name, coldim, values, registry=None, addRegistry=True):
        self.name = name
        self.coldim = int(coldim)
        self.registry = registry

        self.values = [] 
        for i, v in enumerate(values):
            self.values.append(Expression("matrix_expr_idx{}_val_{}".format(i, name), upgradeToStringExpression(registry, v), registry=registry))

        self.values_asarray = _np.array(self.values, dtype=_np.object_)
        if self.coldim > 1:
            self.values_asarray = self.values_asarray.reshape(self.coldim, int(len(values)/self.coldim))

        if registry and addRegistry:
            self.registry.addDefine(self)
            
    def eval(self):
        """ 
        Evaluate matrix

        :return: numerical evaluation of matrix
        :rtype: numpy.array
        """
        a = _np.array([ e.eval() for e in self.values ])
        a = a.reshape(self.coldim,int(len(a)/self.coldim))
        return a

    def __repr__(self):
        return "Matrix : {} = {} {}".format(self.name, str(self.coldim), str(self.values))

    def __getitem__(self, key):
        if self.name in self.registry.defineDict:
            stridx = ','.join([str(v+1) for v in key])
            return Expression("dummy_name", self.name+"["+stridx+"]", self.registry, False)
        else:
            return self.values_asarray[key]


def MatrixFromVectors(e, v, name, registry, eunit='eV', vunit=''):
    """
    Creates a GDML Matrix from an energy and a value vector

    :param name: of matrix of registry
    :type  name: str
    :param e: energy list/vector in units of eunit
    :type e: list or numpy.array - shape (1,)
    :param v: value list/vector in units of vunit
    :type v: list or numpy.array - shape (1,)
    :param registry: for storing define
    :type registry: Registry
    :param eunit: unit for the energy vector (default: eV)
    :type eunit: str
    :param vunit: unit for the value vector (default: unitless)
    :type vunit: str
    """
    assert(len(e) == len(v))
    eunit = '*'+eunit if eunit != '' else ''
    vunit = '*'+vunit if vunit != '' else ''

    e = [ str(x)+eunit for x in e ]
    v = [ str(x)+vunit for x in v ]

    res = e+v
    res[::2] = e
    res[1::2] = v
    return Matrix(name, 2, res, registry)


class Auxiliary:
    """
    Auxiliary information container object
    """
    # Note that no interpreting or processing is done for auxiliary information
    def __init__(self, auxtype, auxvalue, registry=None, unit="", addRegistry=True):
        self.auxtype = str(auxtype)
        self.auxvalue = str(auxvalue)
        self.auxunit = str(unit)
        self.subaux = []
        self.registry = registry
        if self.registry and addRegistry:
            self.registry.addAuxiliary(self)

    def addSubAuxiliary(self, aux):
        """
        Add a sub-auxiliary inside the scope of the current auxiliary

        :param aux: auxiliary definition
        :type aux: object, gdml.Defines.Auxiliary
        """
        if not isinstance(aux, Auxiliary):
            raise ValueError("Added object must be a gdml.Defines.Auxiliary instance.")
        self.subaux.append(aux)

