import pyg4ometry

def Test(vis = False, interactive=False):
    # Loading
    reader = pyg4ometry.gdml.Reader("001_002_one_of_each.gdml")
    registry = reader.getRegistry()

    # World logical
    worldLogical = registry.getWorldVolume()

    # Visualisation
    v = None
    if vis :
        v = pyg4ometry.visualisation.VtkViewer()
        v.setCutterOrigin('z', [0,0,1400])
        v.addLogicalVolume(registry.getWorldVolume())
        v.view(interactive=interactive)

    # Render writer
    #rw = pyg4ometry.visualisation.RenderWriter()
    #rw.addLogicalVolumeRecursive(worldLogical)
    #rw.write("T011_renderWriter")
    return v

if __name__ == '__main__':
   Test()
