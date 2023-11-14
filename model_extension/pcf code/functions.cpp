// This file contains the routines 

#include "functions.h"
#include "bincontainer.h"

// compute g(r): pair correlation function, radial distribution function
void compute_gr(int flag, vector<BINCONTAINER>& gr, unsigned int ngr, vector<PARTICLE>& ljatom, double bx, double by, double bz, double bin_width, double bulk_density)
{
  if (flag == 0)	// initialize
  {
    ngr=0;		// number of gr samples
    unsigned int number_of_bins = int((bz/2.0)/bin_width);
    cout << "number of bins " << number_of_bins << endl;
    gr.resize(number_of_bins);
    for (unsigned int i = 0; i < number_of_bins; i++)
    {
      gr[i].number = i+1;
      gr[i].width = bin_width;
      gr[i].position = (gr[i].width)*(i+0.5);
      gr[i].population = 0.0;
    }
  }
  
  if (flag == 1)	// sample and create histogram
  {
    for (unsigned int i = 0; i < ljatom.size()-1; i++)
    {
      for (unsigned int j = i+1; j < ljatom.size(); j++)
      {
        VECTOR3D r_vec = ljatom[i].posvec - ljatom[j].posvec;
        if (r_vec.x>bx/2) r_vec.x -= bx;
        if (r_vec.x<-bx/2) r_vec.x += bx;
        if (r_vec.y>by/2) r_vec.y -= by;
        if (r_vec.y<-by/2) r_vec.y += by;
        if (r_vec.z>bz/2) r_vec.z -= bz;
        if (r_vec.z<-bz/2) r_vec.z += bz;
        
        double r=r_vec.Magnitude();
        
        if (r < bz/2.0)
        {
            int bin_number = ceil((r/bin_width));
            gr[bin_number - 1].population = gr[bin_number - 1].population + 2;
        }
      }
    }
  }
  
  if (flag == 2)	// determine g(r) after proper normalization
  {
    cout << endl;
    cout << "gr calculation ends " << endl;
    unsigned int number_of_bins = int((bz/2.0)/bin_width);
    ofstream output_gr("gr.out", ios::out);
    for (unsigned int b = 0; b < number_of_bins; b++)
    {
      double r = gr[b].position;
      double vol_bin = (4.0/3.0)*3.14*bin_width*bin_width*bin_width*(3*(r/bin_width)*(r/bin_width) + 3*r/bin_width + 1);
      double nid = vol_bin*bulk_density;
      gr[b].population = gr[b].population / ljatom.size();
      gr[b].population = gr[b].population / ngr;
      gr[b].population = gr[b].population / nid;
      output_gr << r << "  " << gr[b].population << endl;
    }
  }
 return; 
}
