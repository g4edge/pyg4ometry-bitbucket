cmake_minimum_required(VERSION 3.20)
project(cgal_c__)

set(CMAKE_CXX_STANDARD 17)

####################
####### Boost
####################
find_package(Boost 1.71.0 QUIET COMPONENTS system) # header only libraries must not be added here
if(${Boost_FOUND})
    message(STATUS "HAVFOUND Boost ${Boost_INCLUDE_DIRS}")
    include_directories(SYSTEM ${Boost_INCLUDE_DIRS})
else()
    message(STATUS "NOTFOUND boost")
endif()

####################
####### CGAL
####################
find_package(CGAL QUIET)
if (CGAL_FOUND)
    # CGAL_ROOT is the root directory of it
    message(STATUS "HAVFOUND CGAL ${CGAL_INCLUDE_DIRS} ${CGAL_ROOT} ${CGAL_LIBRARIES}")
    include_directories(SYSTEM ${Boost_INCLUDE_DIRS})
else()
    message(STATUS "NOTFOUND CGAL")
endif()

####################
####### mfpr
####################
find_package(MPFR QUIET)

####################
####### gmp
####################
find_package(GMP QUIET)

####################
#######  Executables
####################

add_executable(cgal_isotropic_remesh isotropic_remesh.cpp)
target_link_directories(cgal_isotropic_remesh PRIVATE ${MPFR_LIBRARIES_DIR} ${GMP_LIBRARIES_DIR})
target_link_libraries(cgal_isotropic_remesh PRIVATE ${MPFR_LIBRARIES} ${GMP_LIBRARIES})

add_executable(cgal_isotropic_remesh_split_long isotropic_remesh_split_long.cpp)
target_link_directories(cgal_isotropic_remesh_split_long PRIVATE ${MPFR_LIBRARIES_DIR} ${GMP_LIBRARIES_DIR})
target_link_libraries(cgal_isotropic_remesh_split_long PRIVATE ${MPFR_LIBRARIES} ${GMP_LIBRARIES})

add_executable(cgal_isotropic_remesh_feature_detect isotropic_remesh_feature_detect.cpp)
target_link_directories(cgal_isotropic_remesh_feature_detect PRIVATE ${MPFR_LIBRARIES_DIR} ${GMP_LIBRARIES_DIR})
target_link_libraries(cgal_isotropic_remesh_feature_detect PRIVATE ${MPFR_LIBRARIES} ${GMP_LIBRARIES})

add_executable(cgal_subdivision_loop subdivision_loop.cpp)
target_link_directories(cgal_subdivision_loop PRIVATE ${MPFR_LIBRARIES_DIR} ${GMP_LIBRARIES_DIR})
target_link_libraries(cgal_subdivision_loop PRIVATE ${MPFR_LIBRARIES} ${GMP_LIBRARIES})