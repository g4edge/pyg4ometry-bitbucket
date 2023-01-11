//
// Created by Stewart Boogert on 08/01/2023.
//

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/Polygon_mesh_processing/detect_features.h>
#include <CGAL/Polygon_mesh_processing/IO/polygon_mesh_io.h>
#include <CGAL/Polygon_mesh_processing/remesh.h>
#include <iostream>
#include <string>

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef CGAL::Surface_mesh<K::Point_3>                      Mesh;
typedef boost::graph_traits<Mesh>::face_descriptor          face_descriptor;
namespace PMP = CGAL::Polygon_mesh_processing;
int main(int argc, char* argv[])
{
    const std::string filename = (argc > 1) ? argv[1] : CGAL::data_file_path("meshes/P.off");
    Mesh mesh;
    if(!PMP::IO::read_polygon_mesh(filename, mesh))
    {
        std::cerr << "Invalid input." << std::endl;
        return 1;
    }

    double target_edge_length = (argc > 2) ? std::stod(std::string(argv[2])) : 2.5;
    unsigned int nb_iter = 3;

    PMP::split_long_edges(edges(mesh), target_edge_length, mesh);

    typedef boost::property_map<Mesh, CGAL::edge_is_feature_t>::type EIFMap;
    typedef boost::property_map<Mesh, CGAL::face_patch_id_t<int> >::type PIMap;
    typedef boost::property_map<Mesh, CGAL::vertex_incident_patches_t<int> >::type VIMap;
    EIFMap eif = get(CGAL::edge_is_feature, mesh);
    PIMap pid = get(CGAL::face_patch_id_t<int>(), mesh);
    VIMap vip = get(CGAL::vertex_incident_patches_t<int>(), mesh);
    std::size_t number_of_patches = PMP::sharp_edges_segmentation(mesh, 60, eif, pid,
                                                                  CGAL::parameters::vertex_incident_patches_map(vip));
    std::size_t nb_sharp_edges = 0;
    for(boost::graph_traits<Mesh>::edge_descriptor e : edges(mesh))
    {
        if(get(eif, e))
            ++nb_sharp_edges;
    }

    for(int i=1;i<=number_of_patches;i++) {
        std::cout << i << std::endl;
        std::vector<face_descriptor> patch;
        for (boost::graph_traits<Mesh>::face_descriptor f: faces(mesh)) {
            if (get(pid, f) == i) {
                patch.push_back(f);
            }
        }

        PMP::isotropic_remeshing(patch, target_edge_length, mesh,
                                 CGAL::parameters::number_of_iterations(nb_iter)
                                         .protect_constraints(true)); //i.e. protect border, here
    }

    std::cout << "This mesh contains " << nb_sharp_edges << " sharp edges" << std::endl;
    std::cout << " and " << number_of_patches << " surface patches." << std::endl;

    std::ofstream ofstr;
    ofstr.open("remesh.off");
    CGAL::IO::write_OFF(ofstr, mesh);
    ofstr.close();

    return 0;
}