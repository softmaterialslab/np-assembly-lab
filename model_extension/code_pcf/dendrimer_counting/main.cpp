// Last update: May 20th, 2024
// This is main.

#include<iostream>
#include<iomanip>
#include<fstream>
#include<cmath>
#include<vector>
#include<assert.h>
#include<string>
#include"particle.h"
#include"bincontainer.h"

using namespace std;

// Fundamental quantities, units:
double pi = 3.141593;	// Pi
double mol = 6.022141e23; // Avogadro's number 
long double unitlength;

// select g(r)
// vlpTypes, vlpOriginType, vlpTargetType
int select_gr(int, int*, int*, long double*, int, int, long double);



//select VLP for dendrimer stats
//for condensed dendrimers
// vlpTypes, vlpOriginType
int select_dend(int, int*);

//for bridging dendrimers
// vlpTypes, vlpOriginType, vlpTargetType
int select_bridging(int, int*, int*);

// compute g(r)
// stage, g(bin), samples, vlps, edge, vlpOrgTy, vlpTarTy, bw, rho_bulk.
void compute_gr(int, vector<BINCONTAINER>&, unsigned int, vector<PARTICLE>&, long double, int, int, double, long double);

//compute dendrimer stats
//in main code

//begin:

int main(int argc, char* argv[]) 
{
  // Input variables
  long double vlp_concentration;
  long double dendrimer_ratio;
  long double dendrimer_concentration;
  long double vlp_diameter;
  long double dend_diameter;
  int total_vlp_number;
  int vlpTypes;

  cout << "\n***\n";
  cout << "This program computes the pair correlation function g(r) between VLPs. \nIt assumes you have generated frame.* files using the LAMMPS-produced dump.melt file containing *all* VLPs. \nFrom the user it will need \n * bulk virus concentration, \n * number of components (variant types) in the mixture, \n * total number of VLPs (summing over all vlp types), \n * total number of time samples (frames), and \n * bin width. \ng(r) is produced for self correlations and cross correlations. Results are normalized by the ideal gas bulk virus concentration and are filed as a function of distance in units of VLP diameter." << endl;
  cout << "For condensed and bridging dendrimer counting, make sut=re to use the dumpAll.melt file containing the dendrimer positions." << endl;
  
  cout << "\n***\n";
  cout << "Physical system details \n * all VLP variants have the same size of 56 nm. \n * we are assuming equal concentrations of different variants, (e.g., 1:1 mixture for a 2-component system) \n * note the mapping --> higher charged variant has a smaller variant type number" << endl;
  
  /* --------- physical system details --------- */
  
  cout << endl << "enter virus diameter in nanometers (common: 56)" << endl;
  cin >> vlp_diameter;
  
  cout << endl << "enter dendrimer in nanometers (common: 6.7)" << endl;
  cin >> dend_diameter;
  
  unitlength = vlp_diameter/1e9;
  
  cout << "unit of length is " << unitlength << " meters" << endl;
  
  cout << "vlp diameter in reduced units is " << vlp_diameter/1e9/unitlength << endl;
  cout << "dendrimer diameter in reduced units is " << dend_diameter/1e9/unitlength << endl;
  
  cout << "enter virus concentration in nanomolars (common: 370, 37, 740)" << endl;
  cin >> vlp_concentration;
  
  cout << "enter dendrimer concentration with respect to virus concentration (common: 100, 1000)" << endl;
  cin >> dendrimer_ratio;
  
  dendrimer_concentration = dendrimer_ratio * vlp_concentration;

  vlp_concentration = vlp_concentration * 1.0e-9 * mol / (1.0e-3) / (1/pow(unitlength,3)); // converting to reduced units
  dendrimer_concentration = dendrimer_concentration * 1.0e-9 * mol / (1.0e-3) / (1/pow(unitlength,3)); // converting to reduced units
  
  cout << "vlp concentration in reduced units is " << vlp_concentration << endl;
  
  cout << "enter total number of VLPs of all types (common: 540, 500, 1500)" << endl;
  cin >> total_vlp_number;
  cout << "total number of VLPs simulated " << total_vlp_number << endl;
  
  long double edge_length = pow(total_vlp_number/vlp_concentration, 1.0/3.0);
  
  cout << endl;
  cout << "I measure simulation box edge length to be " << edge_length << endl;
  
  cout << "Enter the simulation box length shown in LAMMPS output (will be similar to above) " << endl;
  cin >> edge_length;
  
  long double simulationBoxVolume = edge_length * edge_length * edge_length;
  
  vlp_concentration = total_vlp_number / simulationBoxVolume; // recomputing vlp_conc to ensure edge length is consistent with vlp number
  
  cout << "Calculations will be computed for less than half the box length, that is < " << 0.5 * edge_length << endl;
  
  cout << "enter number of VLP types / components (common: 1 OR 2 OR 3 OR 4; example: 4-component mixture has EEE2, E2, Q2, K2)" << endl;
  cin >> vlpTypes;
  cout << "solution has " << vlpTypes << " variants (note: we are assuming equal concentrations of different variants, e.g., 1:1 mixture for a 2-component system)" << endl;
  
  long double vlp_concentration_per_variant = vlp_concentration / vlpTypes;
  
  long double bulk_density_per_variant_for_norm = (total_vlp_number / vlpTypes - 1) / simulationBoxVolume; // (N-1) / V is the ideal gas density to be used for normalizing g(r)

  /* --------- Choice of operations --------- */
  int PCF_answer; // asks if user wants to calculate pcf
  int dend_answer; //asks if user wants to count dendrimers
  int condensed_answer; //asks if user wants to count condensed dendrimers
  int bridging_answer;  //asks if user wants to count bridging dendrimers
  
  double threshold_distance;
  
  cout << "Do you wish to calculate any PCFs between VLPs (not recommended with dumpAll.melt file)? enter YES = 1 or NO = 0" << endl;
  cin >> PCF_answer;
  if (PCF_answer == 1)
  {
	  cout << "gr calculations will be performed" << endl;
  }
  else if (PCF_answer == 0)
  {
	  cout << "gr will not be calculated" << endl;
  }
  else 
  {
	  cout << "invalid answer ...exiting..." << endl;
	  return(0);
  }
  
  cout << "Do you wish to calculate dendrimer statistics (dumpAll.melt file REQUIRED)? enter YES = 1 or NO = 0" << endl;
  cin >> dend_answer;
  if (dend_answer == 1)
  {
	  cout << "Dendrimer counting will be performed." << endl;
      double threshold_factor;
      cout << "enter threshold factor that will multiply the touch distance between vlp and linker (1, 1.05, etc.)" << endl;
      cin >> threshold_factor;
      threshold_distance = threshold_factor * 0.5 * (vlp_diameter+dend_diameter)/1e9/unitlength;
      cout << "threshold distance in reduced units is: " << threshold_distance << endl;
	  
	  cout << "Perform counting of condensed dendrimers for a specific VLP type? enter YES = 1 or NO = 0" << endl;
	  cin >> condensed_answer;
	  
	  cout << "Perform counting of bridging dendrimers? enter YES = 1 or NO = 0" << endl;
	  cin >> bridging_answer;
  }
  else if (PCF_answer == 0)
  {
	  cout << "dendrimers will not be counted" << endl;

  }
  else 
  {
	  cout << "invalid answer ...exiting..." << endl;
	  return(0);
  }
   

    
  /* --------- dataset details & preparation --------- */
  
  cout << "\n***\n";
  cout << "Dataset and binning details... " << endl;
  //cout << "\n * assumed you have checked the frequency of obtaining time snapshots (frames) in the simulation (common: 1000, 5000 steps). \n * assumed: first frame number is 1" << endl;
  
  int data_collect_frequency = 1; 
  int start_filenumber = 1;
  int samples = 0;
  int totalframes = 1000;
  double bin_width = 0.01;
  int skipFrames = 1;

  cout << "\nenter the total number of frames (common: 1000, 4000; verify they are there!) " << endl;
  cin >> totalframes;
  cout << "\nenter the start frame number (common: 1, 200000) " << endl;
  cin >> start_filenumber;
  cout << "enter the frame separation steps (common: 1, 1000) " << endl;
  cin >> data_collect_frequency;
  cout << "enter the number of frames you want to skip (common: 1, means no frame skipped; 10)" << endl;
  cin >> skipFrames;
  
  if (PCF_answer == 1)
  {
  cout << "enter bin width (common: 0.01, 0.005, 0.001)" << endl;
  cin >> bin_width;
  }
  
  bool atleastonefile = false;
  
  vector<PARTICLE> dummy_vlp;
  unsigned int dummy_samples;
  vector<BINCONTAINER> gr;
  int vlpOriginType, vlpTargetType;
  
  //string grType;
  //int selfType, crossOriginType, crossTargetType;

  
  if (PCF_answer == 1)
  {
  
	int grSelection = select_gr(vlpTypes, &vlpOriginType, &vlpTargetType, &bulk_density_per_variant_for_norm, total_vlp_number, vlpTypes, simulationBoxVolume);
	if (grSelection == 0) 
	{
      cout << "\nsomething is wrong--> check gr info...exiting..." << endl;
      return 0;
    }
  
	compute_gr(0,gr,dummy_samples,dummy_vlp,edge_length,vlpOriginType,vlpTargetType,bin_width,bulk_density_per_variant_for_norm);
  
	for (unsigned int i = 0; i < totalframes; i++)  
	{
    vector<PARTICLE> vlp; // all particles in the system
    int col1, col2; // id, type
    double col3, col4, col5; // x, y, z
    
    char filename[100];
    int filenumber = start_filenumber + i*data_collect_frequency;
    
    if (filenumber%skipFrames !=0) continue; // skip every skipFrames
    
    sprintf(filename, "frame%d", filenumber);
    ifstream file(filename, ios::in); // reading data from a file
    if (!file) 
    {
      cout << "File could not be opened" << endl;
      continue;
    }
    else if (filenumber%100==0)
      cout << "read frame" << filenumber << endl;
    
    samples++;
    
    for (int i = 1; i <= 9; i++)
    {
      string dummyline;
      getline(file, dummyline); // ignoring the first 9 lines that act as dummylines
    }
    
    while (file >> col1 >> col2 >> col3 >> col4 >> col5)
    {
      PARTICLE myparticle = PARTICLE(col1, col2, VECTOR3D(col3, col4, col5));
      vlp.push_back(myparticle);
    }
    
    compute_gr(1,gr,dummy_samples,vlp,edge_length,vlpOriginType,vlpTargetType,bin_width,bulk_density_per_variant_for_norm);
  }
  
	cout << "\nnumber of time snapshots (samples) used to compute g(r): " << samples << endl;
	dummy_vlp.resize(total_vlp_number/vlpTypes); // this is to send the right number of variant-specific particles; only true for 1:1:1:... mixtures
	cout << "number of vlps used to take the average: " << dummy_vlp.size() << endl;
	cout << "bulk density used to normalize: " << bulk_density_per_variant_for_norm << endl;
	cout << "vlp concentration per type (thermodynamic limit result): " << vlp_concentration_per_variant << endl;
  
	compute_gr(2,gr,samples,dummy_vlp,edge_length,vlpOriginType,vlpTargetType,bin_width,bulk_density_per_variant_for_norm);
  }

  if (condensed_answer == 1)
  {
    int dend_selection = select_dend(vlpTypes, &vlpOriginType);
    int framecountLinker = 0; // counting for all frames
	                
    if (dend_selection == 0) 
	{
      cout << "\nsomething is wrong--> check gr info...exiting..." << endl;
      return 0;
    }	
	
	for (unsigned int i = 0; i < totalframes; i++)  
	{
    vector<PARTICLE> vlp_specific; // specific VLPs
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
      cout << "File could not be opened" << endl;
      continue;
    }
    else if (filenumber%10==0)
      cout << "read frame" << filenumber << endl;
    
    samples++;
    
    for (int i = 1; i <= 9; i++)
    {
      string dummyline;
      getline(file, dummyline); // ignoring the first 9 lines that act as dummylines
    }
    
    while (file >> col1 >> col2 >> col3 >> col4 >> col5)
    {
      PARTICLE myparticle = PARTICLE(col1, col2, VECTOR3D(col3, col4, col5));
      if (col2 == vlpOriginType)
          vlp_specific.push_back(myparticle);
      else if (col2 == 3)
          linker.push_back(myparticle);
    }
	
	int countLinker = 0; // counting only the condensed linkers for one frame
    for (int i = 0; i < vlp_specific.size(); i++)
    {
        for (int j = 0; j < linker.size(); j++)
        {
            double distance = (vlp_specific[i].posvec - linker[j].posvec).Magnitude();
            if (distance < threshold_distance)
                countLinker++;
        }        
    }
    
    countLinker = countLinker / vlp_specific.size();    
    framecountLinker = framecountLinker + countLinker;
		
  }
  
  cout << "number of condensed linkers per VLP of type:" << vlpOriginType << " are " << framecountLinker/totalframes << endl;
  cout << "\n";
  }
  
  if (bridging_answer ==1)
  {
	int bridging_selection = select_bridging(vlpTypes, &vlpOriginType, &vlpTargetType);
    int framecountLinker = 0; // counting for all frames
	                
    if (bridging_selection == 0) 
	{
      cout << "\nsomething is wrong--> ...exiting..." << endl;
      return 0;
    }	
	
	for (unsigned int i = 0; i < totalframes; i++)  
	{
    vector<PARTICLE> vlp; //all VLPs in the system
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
      cout << "File could not be opened" << endl;
      continue;
    }
    else if (filenumber%10==0)
      cout << "read frame" << filenumber << endl;
    
    samples++;
    
    for (int i = 1; i <= 9; i++)
    {
      string dummyline;
      getline(file, dummyline); // ignoring the first 9 lines that act as dummylines
    }
    
    while (file >> col1 >> col2 >> col3 >> col4 >> col5)
    {
      PARTICLE myparticle = PARTICLE(col1, col2, VECTOR3D(col3, col4, col5));
      if (col2 !=3)
          vlp.push_back(myparticle);

      else if (col2 == 3)
          linker.push_back(myparticle);
    }
	
	int countLinker = 0; // counting only the condensed linkers for one frame
	int counter = 0;
	
    for (int i = 0; i < linker.size(); i++) //sweep over all linkers
    {
		int counter;
        for (int j = 0; j < vlp.size(); j++)
        {
			if (vlpOriginType == vlpTargetType)
			{
				counter = i+1;
			}
			else
			{
				counter = 0;
			}
			
			double distance = (vlp[i].posvec - linker[j].posvec).Magnitude();
			if (distance < threshold_distance)
			{
				for (unsigned int j = counter; j < vlp.size(); j++)
				{
					if (vlp[i].ty != vlpOriginType || vlp[j].ty != vlpTargetType)
					{
						continue;
					}
					double distance = (vlp[i].posvec - linker[j].posvec).Magnitude();
					if (distance < threshold_distance)
						countLinker++;
				}
			}
		}
    }			
    
    countLinker = countLinker / linker.size();    
    framecountLinker = framecountLinker + countLinker;
		
  }    
  
  cout << "average number of bridging linkers per VLP of type" << vlpOriginType << "and type " << vlpTargetType << " is " << framecountLinker/totalframes << endl;
  cout << "\n";
  }
  
  return 0;
} 
// End of main
