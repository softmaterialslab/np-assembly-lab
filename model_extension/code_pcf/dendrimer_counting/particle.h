// This is the particle class

#ifndef _PARTICLE_H
#define _PARTICLE_H

#include "vector3d.h"

class PARTICLE 
{
  public:

  // members
  int id;		// id of the particle
  int ty;	    // type of the particle
  //double mass; 		// mass of the particle
  VECTOR3D posvec;	// position vector of the particle
    
  // member functions
  
  // make a particle	// this function in C++ is known as a constructor
  PARTICLE(int initial_id = 1, int initial_ty = 1, VECTOR3D initial_position = VECTOR3D(0,0,0))
  {
    id = initial_id;
    ty = initial_ty;
    //mass = initial_mass;
    posvec = initial_position;
  }
  
};

#endif
