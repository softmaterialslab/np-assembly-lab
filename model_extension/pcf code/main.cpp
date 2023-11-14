// Last update: January 06, 2017
// This is main.

#include<iostream>
#include<iomanip>
#include<fstream>
#include<cmath>
#include<vector>
#include "particle.h"
#include "bincontainer.h"

using namespace std;

void compute_gr(int, vector<BINCONTAINER>&, unsigned int, vector<PARTICLE>&, double, double, double, double, double);

int main(int argc, char* argv[]) 
{
  // Input variables
  const double pi = 3.141593;	// Pi
  const double mol = 6.0e23;

  long double ljatom_density = 0.0782;	// mass density

  cout << "*********" << endl;
  cout << "This program computes the pair correlation function or radial distribution function g(r) for a fluid system. \n It assumes you have generated data.coords.all files using the LAMMPS template shared. \n From the user it will need \n * the (bulk) density of the fluid, \n * the first coordinates (coords) file number, \n * total number of samples they want to use to compute g(r), and \n * bin width. \n The program then scans all the files, computes pair-wise distances, and bins the data. \nFinally, it produces g(r) with bulk density as the normalization (ideal gas result)." << endl;
  cout << "*********" << endl;
  cout << endl;
  
  //cout << "enter density (use the density associated with the simulation that produced all the particle positions data)" << endl;
  //cin >> ljatom_density;

  // could compute edge length using lattice size and FCC initialization
//  long double el_lattice = 5;
//  long double edge_length = el_lattice * pow(4/ljatom_density,1.0/3.0);
  
  // or, use number of atoms
  int number_ljatom = 108;
  long double edge_length = pow(108/ljatom_density, 1.0/3.0);
  
  cout << endl;
  cout << "I measure box length to be " << edge_length << endl;
  cout << "g(r) will be computed for less than half the box length, that is < " << 0.5 * edge_length << endl;
  cout << "number of atoms in the main cell of the simulation box " << number_ljatom << endl;
  
  double bx, by, bz;		// box edge lengths
  
  bx = edge_length; 
  by = edge_length;
  bz = edge_length;
  
  // gr begins
  int data_collect_frequency = 1;
  int start_filenumber = 1;	// default

  //cout << endl;
  //cout << "enter the first data.coords.all file number (default choice: 20000 ; verify the file data.coords.all.20000 exists) " << endl;
  //cin >> start_filenumber;
  
  int samples = 100;		// default

  //cout << endl;
  //cout << "enter the total number of time snapshots / samples / data.coords.all files (default: 201 ; verify that there are at least 201 data.coords.all files in the folder) " << endl;
  //cout << "I have assumed that the sample frequency is 1000, that is data.coords.all files are separated by 1000 steps" << endl;
  //cin >> samples;
  
  double bin_width = 0.01;	// default

  //cout << endl;
  //cout << "enter bin width (0.01 should be good, but may need to be smaller)" << endl;
  //cin >> bin_width;

  bool atleastonefile = false;
  
  vector<PARTICLE> dummy_ljatom;
  vector<BINCONTAINER> gr;
  
  compute_gr(0,gr,0,dummy_ljatom,bx,by,bz,bin_width,ljatom_density);
  
  for (unsigned int i = 0; i < samples; i++)  
  {
    vector<PARTICLE> ljatom;	// all particles in the system
    int col1, col2; // id, type
    double col3, col4, col5; // x, y, z
    
    char filename[100];
    int filenumber = start_filenumber + i;//*data_collect_frequency;
    sprintf(filename, "data%d", filenumber);
    ifstream file(filename, ios::in); // reading data from a file
    if (!file) 
    {
      cout << "File could not be opened" << endl;
      continue;
    }
    else
      cout << "read file data.coords.all." << filenumber << endl;
    
    for (int i = 1; i <= 9; i++)
    {
      string dummyline;
      getline(file, dummyline); // ignoring the first 9 lines that act as dummylines
    }
    
    while (file >> col1 >> col2 >> col3 >> col4 >> col5)
    {
      PARTICLE myparticle = PARTICLE(col1, col2, VECTOR3D(col3, col4, col5));
      ljatom.push_back(myparticle);
    }
    
    compute_gr(1,gr,samples,ljatom,bx,by,bz,bin_width,ljatom_density);
  }
  
  vector<PARTICLE> ljatom;
  ljatom.resize(number_ljatom);
  compute_gr(2,gr,samples,ljatom,bx,by,bz,bin_width,ljatom_density);
    
  return 0;
} 
// End of main
