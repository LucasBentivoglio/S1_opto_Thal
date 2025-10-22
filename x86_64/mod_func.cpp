#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _CaDynamics_DC0_reg(void);
extern void _Ca_HVA2_reg(void);
extern void _Ca_LVAst_reg(void);
extern void _DetAMPANMDA_reg(void);
extern void _DetGABAAB_reg(void);
extern void _Ih_reg(void);
extern void _kd_reg(void);
extern void _kdr_reg(void);
extern void _KdShu2007_reg(void);
extern void _K_Pst_reg(void);
extern void _K_Tst_reg(void);
extern void _Kv3_1_reg(void);
extern void _MyExp2SynBB_reg(void);
extern void _my_exp2syn_reg(void);
extern void _MyExp2SynNMDABB_reg(void);
extern void _Nap_Et2_reg(void);
extern void _nas_reg(void);
extern void _NaTg_reg(void);
extern void _NaV_reg(void);
extern void _ProbAMPANMDA_EMS_reg(void);
extern void _ProbGABAAB_EMS_reg(void);
extern void _SK_E2_reg(void);
extern void _SKv3_1_fs2_reg(void);
extern void _SKv3_1_fs_reg(void);
extern void _SKv3_1_reg(void);
extern void _StochKv3_reg(void);
extern void _TTXDynamicsSwitch_reg(void);
extern void _vecstim_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"modfiles//CaDynamics_DC0.mod\"");
    fprintf(stderr, " \"modfiles//Ca_HVA2.mod\"");
    fprintf(stderr, " \"modfiles//Ca_LVAst.mod\"");
    fprintf(stderr, " \"modfiles//DetAMPANMDA.mod\"");
    fprintf(stderr, " \"modfiles//DetGABAAB.mod\"");
    fprintf(stderr, " \"modfiles//Ih.mod\"");
    fprintf(stderr, " \"modfiles//kd.mod\"");
    fprintf(stderr, " \"modfiles//kdr.mod\"");
    fprintf(stderr, " \"modfiles//KdShu2007.mod\"");
    fprintf(stderr, " \"modfiles//K_Pst.mod\"");
    fprintf(stderr, " \"modfiles//K_Tst.mod\"");
    fprintf(stderr, " \"modfiles//Kv3_1.mod\"");
    fprintf(stderr, " \"modfiles//MyExp2SynBB.mod\"");
    fprintf(stderr, " \"modfiles//my_exp2syn.mod\"");
    fprintf(stderr, " \"modfiles//MyExp2SynNMDABB.mod\"");
    fprintf(stderr, " \"modfiles//Nap_Et2.mod\"");
    fprintf(stderr, " \"modfiles//nas.mod\"");
    fprintf(stderr, " \"modfiles//NaTg.mod\"");
    fprintf(stderr, " \"modfiles//NaV.mod\"");
    fprintf(stderr, " \"modfiles//ProbAMPANMDA_EMS.mod\"");
    fprintf(stderr, " \"modfiles//ProbGABAAB_EMS.mod\"");
    fprintf(stderr, " \"modfiles//SK_E2.mod\"");
    fprintf(stderr, " \"modfiles//SKv3_1_fs2.mod\"");
    fprintf(stderr, " \"modfiles//SKv3_1_fs.mod\"");
    fprintf(stderr, " \"modfiles//SKv3_1.mod\"");
    fprintf(stderr, " \"modfiles//StochKv3.mod\"");
    fprintf(stderr, " \"modfiles//TTXDynamicsSwitch.mod\"");
    fprintf(stderr, " \"modfiles//vecstim.mod\"");
    fprintf(stderr, "\n");
  }
  _CaDynamics_DC0_reg();
  _Ca_HVA2_reg();
  _Ca_LVAst_reg();
  _DetAMPANMDA_reg();
  _DetGABAAB_reg();
  _Ih_reg();
  _kd_reg();
  _kdr_reg();
  _KdShu2007_reg();
  _K_Pst_reg();
  _K_Tst_reg();
  _Kv3_1_reg();
  _MyExp2SynBB_reg();
  _my_exp2syn_reg();
  _MyExp2SynNMDABB_reg();
  _Nap_Et2_reg();
  _nas_reg();
  _NaTg_reg();
  _NaV_reg();
  _ProbAMPANMDA_EMS_reg();
  _ProbGABAAB_EMS_reg();
  _SK_E2_reg();
  _SKv3_1_fs2_reg();
  _SKv3_1_fs_reg();
  _SKv3_1_reg();
  _StochKv3_reg();
  _TTXDynamicsSwitch_reg();
  _vecstim_reg();
}

#if defined(__cplusplus)
}
#endif
