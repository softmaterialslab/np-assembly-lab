// This file contains the routines 

#include "functions.h"
#include "bincontainer.h"

extern double pi, mol;
extern long double unitlength;

// compute g(r): pair correlation function
void compute_gr(int flag, vector<BINCONTAINER>& gr, unsigned int ngr, vector<PARTICLE>& vlp, long double L, int vlpOriginType, int vlpTargetType, double bin_width, long double bulk_density)
{
  if (flag == 0)	// initialize
  {
    unsigned int number_of_bins = int((L/2.0)/bin_width);
    cout << "number of bins " << number_of_bins << endl;
    gr.resize(number_of_bins);
    for (unsigned int i = 0; i < number_of_bins; i++)
    {
        gr[i].number = i+1;
        gr[i].width = bin_width;
        gr[i].position = (gr[i].width)*(i); // bin position is defined with left edge position, this makes volume calculation accurate
        //gr[i].position = (gr[i].width)*(i+0.5); 
        gr[i].population = 0.0;
    }
  }
  
  if (flag == 1)	// sample and create histogram
  {
    //for (unsigned int i = 0; i < vlp.size()-1; i++) WHY -1!!! it should not matter
      
    int counter;
    int addMember;
      
    for (unsigned int i = 0; i < vlp.size(); i++)    
    {
      if (vlpOriginType == vlpTargetType)
      {
          counter = i+1;
          addMember = 2;
      }
      else
      { 
          counter = 0;
          addMember = 1;
      }
      for (unsigned int j = counter; j < vlp.size(); j++)
      {
          if (vlp[i].ty != vlpOriginType || vlp[j].ty != vlpTargetType)
          {
              continue;
          }
          
          VECTOR3D r_vec = vlp[i].posvec - vlp[j].posvec;
          if (r_vec.x>L/2) r_vec.x -= L;
          if (r_vec.x<-L/2) r_vec.x += L;
          if (r_vec.y>L/2) r_vec.y -= L;
          if (r_vec.y<-L/2) r_vec.y += L;
          if (r_vec.z>L/2) r_vec.z -= L;
          if (r_vec.z<-L/2) r_vec.z += L;
          
          double r = r_vec.Magnitude();
          if (r < L/2.0)
          {
              int bin_number = ceil((r/bin_width));
              gr[bin_number - 1].population = gr[bin_number - 1].population + addMember;
          }
        }
      }
    }
  
  if (flag == 2)	// determine g(r) after proper normalization
  {
    cout << endl;
    cout << "gr calculation ends " << endl;
    unsigned int number_of_bins = int((L/2.0)/bin_width);
    char grFile[200];
    sprintf(grFile, "gr_%d_%d.out", vlpOriginType, vlpTargetType);
    ofstream output_gr(grFile, ios::out);
    for (unsigned int b = 0; b < number_of_bins; b++)
    {
      double r = gr[b].position;
      long double vol_bin = (4.0/3.0)*pi*(3*r*r*bin_width + 3*r*bin_width*bin_width + bin_width*bin_width*bin_width);
      
      long double nid = vol_bin*bulk_density;
      //double ideal_gas_density = (vlp.size()-1)/(L*L*L);
      //long double nid = vol_bin*ideal_gas_density;
      
      gr[b].population = gr[b].population / vlp.size();
      gr[b].population = gr[b].population / ngr;
      gr[b].population = gr[b].population / nid;
      
      // taking into account the presence of linkers
      //gr[b].population = gr[b].population / (1 - 0.00350894); // 1/(1 - clinker * vlinker)
      
      //double rCenter = r;      
      double rCenter = r + 0.5*gr[b].width;
      output_gr << rCenter << "  " << gr[b].population << endl;
    }
  }
  return; 
}

// select which gr to compute
int select_gr(int vlpTypes, int *vlpOriginType, int *vlpTargetType, long double *bulk_density_per_variant_for_norm, int N, int variants, long double V)
{
  string grType;
  int selfType, crossOriginType, crossTargetType;
  
  if (vlpTypes == 1)
  {
      cout << "\nfor a 1-component system, there is only 1 self correlation function (g11), proceeding to compute that..." << endl;
      *vlpOriginType = 1;
      *vlpTargetType = *vlpOriginType;
  }
  else if (vlpTypes == 2)
  {
      cout << "\nfor a 2-component system, there are 2 self correlation functions (g11, g22) and 1 cross correlation function (g12)" << endl;
      cout << "which correlation function you want to compute: self or cross?" << endl;
      cin >> grType;
      if (grType == "self")
      {
          cout << "which self correlation you want to compute: between VLP type 1 and VLP type 1 (enter 1) OR VLP type 2 and VLP type 2 (enter 2)?" << endl;
          cin >> selfType;
          *vlpOriginType = selfType;
          *vlpTargetType = *vlpOriginType;
      }
      else if (grType == "cross")
      {
          *vlpOriginType = 1;
          *vlpTargetType = 2;
          *bulk_density_per_variant_for_norm = (N*1.0/variants)/V;
      }
      else
      {
          cout << "\nsomething is wrong--> check gr info...exiting..." << endl;
          return(0);
      }
  }
  else if (vlpTypes == 3)
  {
      cout << "\nfor a 3-component system, there are 3 self correlation functions (g11, g22, g33) and 3 cross correlation function (g12, g13, g23)" << endl;
      cout << "which correlation function you want to compute: self or cross?" << endl;
      cin >> grType;
      if (grType == "self")
      {
          cout << "which self correlation you want to compute: between VLP type 1 and VLP type 1 (enter 1) OR VLP type 2 and VLP type 2 (enter 2) OR between VLP type 3 and VLP type 3 (enter 4 <-- THIS IS NOT A TYPO)?" << endl;
          cin >> selfType;
          *vlpOriginType = selfType;
          *vlpTargetType = *vlpOriginType;
      }
      else if (grType == "cross")
      {
          cout << "which cross correlation you want to compute: between VLP type 1 and VLP type 2 (enter 1 ENTER 2) OR VLP type 1 and VLP type 3 (enter 1 ENTER 4) OR between VLP type 2 and VLP type 3 (enter 2 ENTER 4)?" << endl;
          cin >> crossOriginType;
          cin >> crossTargetType;
          *vlpOriginType = crossOriginType;
          *vlpTargetType = crossTargetType;
          *bulk_density_per_variant_for_norm = (N*1.0/variants)/V;
      }
      else
      {
          cout << "\nsomething is wrong--> check gr info...exiting..." << endl;
          return(0);
      }
  }
  else if (vlpTypes == 4)
  {
      cout << "\nfor a 4-component system, there are 4 self correlation functions (g11, g22, g33, g44) and 6 cross correlation function (g12, g13, g14, g23, g24, g34)" << endl;
      cout << "which correlation function you want to compute: self or cross?" << endl;
      cin >> grType;
      if (grType == "self")
      {
          cout << "which self correlation you want to compute: between VLP type 1 and VLP type 1 (enter 1) OR VLP type 2 and VLP type 2 (enter 2) OR between VLP type 3 and VLP type 3 (enter 4 <-- THIS IS NOT A TYPO) OR between VLP type 5 and VLP type 5 (enter 5 <-- THIS IS NOT A TYPO)?" << endl;
          cin >> selfType;
          *vlpOriginType = selfType;
          *vlpTargetType = *vlpOriginType;
      }
      else if (grType == "cross")
      {
          cout << "which cross correlation you want to compute: between VLP type 1 and VLP type 2 (enter 1 ENTER 2) OR VLP type 1 and VLP type 3 (enter 1 ENTER 4) OR VLP type 1 and VLP type 4 (enter 1 ENTER 5) OR between VLP type 2 and VLP type 3 (enter 2 ENTER 4) OR between VLP type 2 and VLP type 4 (enter 2 ENTER 5) OR between VLP type 2 and VLP type 4 (enter 2 ENTER 5) OR between VLP type 3 and VLP type 4 (enter 4 ENTER 5)?" << endl;
          cin >> crossOriginType;
          cin >> crossTargetType;
          *vlpOriginType = crossOriginType;
          *vlpTargetType = crossTargetType;
          *bulk_density_per_variant_for_norm = (N*1.0/variants)/V;
      }
      else
      {
          cout << "\nsomething is wrong--> check gr info...exiting..." << endl;
          return(0);
      }	  
  }
  cout << "\ncomputing " << grType << " g(r) between VLP type " <<  *vlpOriginType << " and VLP type " << *vlpTargetType << endl;
  return(1);
}

//compute dendrimer statistics
void calculate_dendrimers(int vlpTypes, int vlpOriginType, int vlpTargetType, double threshold_distance, int total_vlp_number, int data_collect_frequency, int start_filenumber, int samples, int totalframes, int skipFrames)
{
	
	int framecountLinkerBridge = 0; // counting for all frames
	int framecountLinkerCondensed = 0; // counting for all frames
	
for (unsigned int i  = 0; i < totalframes; i++)  
	{
    vector<PARTICLE> vlp; // all VLPs in system
    vector<PARTICLE> linker;
    int col1, col2; // id, type
    double col3, col4, col5; // x, y, z
        
    char filename[100];
    int filenumber = start_filenumber + i*data_collect_frequency;
    
    if (filenumber%skipFrames !=0) continue; // skip every skipFrames
    
    sprintf(filename, "frame%d", filenumber);
    ifstream file(filename, ios::in); // reading data from a file
    if (!file) 
    {
      //cout << "File could not be opened" << endl;
      continue;
    }
    else if (filenumber%10==0)
      //cout << "read frame" << filenumber << endl;
    
    samples++;
    
    for (int i = 1; i <= 9; i++)
    {
      string dummyline;
      getline(file, dummyline); // ignoring the first 9 lines that act as dummylines
    }
    
    while (file >> col1 >> col2 >> col3 >> col4 >> col5)
    {
	  PARTICLE myparticle = PARTICLE(col1, col2, VECTOR3D(col3, col4, col5));
	  if (vlpTypes != 1)
	  {
		
			if (col2 != 3)
				vlp.push_back(myparticle);
			else if (col2 == 3)
				linker.push_back(myparticle);  
	  }
	  else if (vlpTypes == 1)
	  {
			if (col2 != 2)
				vlp.push_back(myparticle);
			else if (col2 == 2)
				linker.push_back(myparticle);		  
	  }
      
    }
	
	int counter;
	int total_bridges = 0; // total number of bridging dendrimers per frame
	int total_condensed = 0; // total number of condensed dendrimers per frame
	
	//cout << "so far so good!" << endl;	
		
    for (int i = 0; i < vlp.size(); i++)
	//for (int i = 0; i < 10; i++)
    {
		//cout << "i = " << i << endl;
		int countLinkerAUX = 0; // counting only the condensed linkers 
		int countLinker = 0; // counting the bridging linkers 
		if (vlpOriginType == vlpTargetType)
		{
			counter = i+1;
		}
		else
		{
			counter = 0;
		}
		
		if (vlp[i].ty != vlpOriginType)
		{
			continue;
		}
			
        for (int j = 0; j < linker.size(); j++)
        {
            double distanceOrigin = (vlp[i].posvec - linker[j].posvec).Magnitude();
            if (distanceOrigin < threshold_distance)
			{
				countLinkerAUX ++;
				//cout << "found condensed dendrimer! loooking if it's a bridging one..." << endl;
				//cout << "counter = " << counter << endl;
				for (int k = counter; k < vlp.size(); k++)	// issue reaching this loop!
				{	
				    if (vlp[i].ty != vlpTargetType)
					{
						continue;
					}
				
					//cout << k << endl;
					double distanceTarget = (vlp[k].posvec - linker[j].posvec).Magnitude();
					if (distanceTarget < threshold_distance)
					{
						//cout << "\nfound one!" << endl;
						countLinker ++;
					}
				}
			}
        } 

	//cout << "for VLP i = " << i << " (of type " << vlp[i].ty << "), " << countLinkerAUX << " condensed dendrimers and "<< countLinker << " bridging dendimers were counted" << endl;
	total_bridges = total_bridges + countLinker ;
	total_condensed = total_condensed + countLinkerAUX ;
    }
	
	int size_pertype = total_vlp_number/vlpTypes;
	
	if (vlpOriginType == vlpTargetType)
	{
		//cout << "Total VLP number is " << size_pertype << endl;
		total_bridges = total_bridges / size_pertype;
		total_condensed = total_condensed / size_pertype;
	}
	
	if (vlpOriginType != vlpTargetType)
	{
		int total_size = 2 * size_pertype;
		//cout << "Total VLP number is " << total_size << endl;
		total_bridges = total_bridges / total_size ;
		total_condensed = total_condensed / total_size ;
	}
	       
        framecountLinkerBridge = framecountLinkerBridge + total_bridges;
	    framecountLinkerCondensed = framecountLinkerCondensed + total_condensed;
	
	}

    if (vlpOriginType == vlpTargetType)
    {
	    cout << "\naverage number of condensed linkers per VLP of type " << vlpOriginType << " is " << framecountLinkerCondensed/totalframes << endl;
    }
  
  cout << "average number of bridging linkers per VLP  between (type " << vlpOriginType << " and type " << vlpTargetType << ") is " << framecountLinkerBridge/totalframes << endl;
}

