//
// Created by Stewart Boogert on 08/01/2023.
//

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/Surface_mesh/IO/OFF.h>
#include <CGAL/Polygon_mesh_processing/remesh.h>
#include <CGAL/Polygon_mesh_processing/border.h>
#include <CGAL/Polygon_mesh_processing/IO/polygon_mesh_io.h>
#include <CGAL/Polygon_mesh_processing/detect_features.h>
#include <boost/iterator/function_output_iterator.hpp>
#include <iostream>
#include <string>
#include <vector>
typedef CGAL::Exact_predicates_inexact_constructions_kernel   K;
typedef CGAL::Surface_mesh<K::Point_3>                        Mesh;
typedef boost::graph_traits<Mesh>::halfedge_descriptor        halfedge_descriptor;
typedef boost::graph_traits<Mesh>::edge_descriptor            edge_descriptor;
namespace PMP = CGAL::Polygon_mesh_processing;
struct halfedge2edge
{
    halfedge2edge(const Mesh& m, std::vector<edge_descriptor>& edges)
            : m_mesh(m), m_edges(edges)
    {}
    void operator()(const halfedge_descriptor& h) const
    {
        m_edges.push_back(edge(h, m_mesh));
    }
    const Mesh& m_mesh;
    std::vector<edge_descriptor>& m_edges;
};

int main(int argc, char* argv[])
{
    const std::string filename = (argc > 1) ? argv[1] : CGAL::data_file_path("pig.off");
    Mesh mesh;
    if(!PMP::IO::read_polygon_mesh(filename, mesh) || !CGAL::is_triangle_mesh(mesh))
    {
        std::cerr << "Invalid input." << std::endl;
        return 1;
    }
    double target_edge_length = (argc > 2) ? std::stod(std::string(argv[2])) : 2;
    unsigned int nb_iter = 3;

    // Constrain edges with a dihedral angle over 60°
    typedef boost::property_map<Mesh, CGAL::edge_is_feature_t>::type EIFMap;
    EIFMap eif = get(CGAL::edge_is_feature, mesh);
    PMP::detect_sharp_edges(mesh, 60, eif);
    int sharp_counter = 0;
    for(edge_descriptor e : edges(mesh))
        if(get(eif, e))
            ++sharp_counter;
    std::cout << sharp_counter << " sharp edges" << std::endl;

    PMP::split_long_edges(edges(mesh), target_edge_length, mesh);

    std::ofstream ofstr;
    ofstr.open("split.off");
    CGAL::IO::write_OFF(ofstr, mesh);
    ofstr.close();

    std::cout << "Start remeshing of " << filename
              << " (" << num_faces(mesh) << " faces)..." << std::endl;
    PMP::isotropic_remeshing(faces(mesh), target_edge_length, mesh,
                             CGAL::parameters::number_of_iterations(nb_iter)
                                     .protect_constraints(true)
                                     .edge_is_constrained_map(eif)); //i.e. protect border, here
    std::cout << "Remeshing done." << std::endl;

    ofstr.open("remesh.off");
    CGAL::IO::write_OFF(ofstr, mesh);
    ofstr.close();


    return 0;
}