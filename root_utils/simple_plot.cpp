#include <iostream>
#include <stdio.h>     
#include <stdlib.h>
//#include <sstream>

#include "TTree.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TStyle.h"
#include "TROOT.h"
#include "TSystem.h"
#include "TCanvas.h"
#include "TFile.h"

// #include "WCSimRootOptions.hh"
// #include "WCSimRootGeom.hh"
// #include "WCSimRootEvent.hh"
//using namespace std;

int simple_plot(const char *filename)
{
  char* wcsimdirenv;
  wcsimdirenv = getenv ("WCSIMDIR");
  if(wcsimdirenv !=  NULL){
    gSystem->Load("${WCSIMDIR}/libWCSimRoot.so");
  }else{
    gSystem->Load("../libWCSimRoot.so");
  }

  TFile * fout = new TFile("plotting_output.root","RECREATE");
  
  TFile * file = new TFile(filename,"read");
  if (!file->IsOpen()){
    cout << "Error, could not open input file: " << filename << endl;
    return -1;
  }
  
  TTree *tree = (TTree*)file->Get("wcsimT");
  const long nevent = tree->GetEntries();

  // Get 20in PMT event
  WCSimRootEvent* wcsimrootsuperevent_20 = new WCSimRootEvent();
  TBranch *branch = tree->GetBranch("wcsimrootevent");
  branch->SetAddress(&wcsimrootsuperevent_20);

  tree->GetBranch("wcsimrootevent")->SetAutoDelete(kTRUE);

  // Get 3in PMT event
  WCSimRootEvent* wcsimrootsuperevent_3 = new WCSimRootEvent();
  TBranch *branch2 = tree->GetBranch("wcsimrootevent2");
  branch2->SetAddress(&wcsimrootsuperevent_3);

  tree->GetBranch("wcsimrootevent2")->SetAutoDelete(kTRUE);

  TTree *geotree = (TTree*)file->Get("wcsimGeoT");
  WCSimRootGeom *geo = 0; 
  geotree->SetBranchAddress("wcsimrootgeom", &geo);
  if (geotree->GetEntries() == 0) {
      exit(9);
  }
  geotree->GetEntry(0);

  WCSimRootTrigger* wcsimrootevent_20, wcsimrootevent_3;

  const float detR = geo->GetWCCylRadius();
  const float detZ = geo->GetWCCylLength();
  TH1F *h_nhits = new TH1F("h_nhits", "nhits; number of hits", 100, 1, -1);
  TH1F *h_hits_time = new TH1F("h_hits_time", "hits_time; hits time [ns]", 100, 1, -1);
  fout->cd(); 
  for (int ievent=0; ievent<10; ievent++){
    tree->GetEntry(ievent);      
    wcsimrootevent_20 = wcsimrootsuperevent_20->GetTrigger(0);

    int ncherenkovdigihits_20 = wcsimrootevent_20->GetNcherenkovdigihits(); 
    
    h_nhits->Fill(ncherenkovdigihits_20);
    string title = "h_hits_map";
    string Ttitle = "h_top_map";
    string Btitle = "h_bott_map";
    title += std::to_string(ievent);
    Ttitle += std::to_string(ievent);
    Btitle += std::to_string(ievent);
    TH2F *h_hits_map = new TH2F("h_hits_map", "hits_map; #phi [rad]; z [cm]", 50, -3.3, 3.3, 50, -3000,3000);
    TH2F *h_top_map = new TH2F("h_top_map", "top_map; x [cm]; y [cm]", 50, -3500, 3500, 50, -3500,3500);
    TH2F *h_bott_map = new TH2F("h_bott_map", "bott_map; x [cm]; y [cm]", 50, -3500, 3500, 50, -3500,3500);

    h_hits_map->SetName(title.c_str());
    h_top_map->SetName(Ttitle.c_str());
    h_bott_map->SetName(Btitle.c_str());

    //int ncherenkovdigihits_slots = wcsimrootevent->GetNcherenkovdigihits_slots();
    //TClonesArray *ncherenkovdigihits_slots = wcsimrootevent->GetCherenkovDigiHits();
    for (int idigi=0;idigi<ncherenkovdigihits_20;idigi++){

      TObject *element = (wcsimrootevent->GetCherenkovDigiHits())->At(idigi);
      if(!element) continue;
      
      WCSimRootCherenkovDigiHit *wcsimrootcherenkovdigihit = 
        dynamic_cast<WCSimRootCherenkovDigiHit*>(element);
      
      h_hits_time->Fill(wcsimrootcherenkovdigihit->GetT());
      int tube_id = wcsimrootcherenkovdigihit->GetTubeId();
      WCSimRootPMT pmt = geo->GetPMT(tube_id - 1);
      float pmt_x = pmt.GetPosition(0);
      float pmt_y = pmt.GetPosition(1);
      float pmt_z = pmt.GetPosition(2);
      float pmt_phi = atan2(pmt_y, pmt_x);
      if( pmt.GetCylLoc() == 1 )
        h_hits_map->Fill(pmt_phi, pmt_z);
      if( pmt.GetCylLoc() == 0 )
        h_top_map->Fill(pmt_x,pmt_y);
      if( pmt.GetCylLoc() == 2 )
        h_bott_map->Fill(pmt_x,pmt_y);
    }
    h_hits_map->Write();
    h_top_map->Write();
    h_bott_map->Write();

    wcsimrootsuperevent->ReInitialize();
    
  } // ievent // End of loop over events

  h_nhits->Write();
  h_hits_time->Write();
  fout->Close();

  return 0;
}