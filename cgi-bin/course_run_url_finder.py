

class duplicate(Exception):
    pass
def find_urls(calendar=None):
    if calendar:
        page_source = calendar_source
    else:
        page_source = timetable_source
        
    page_source = page_source.replace('&amp;', '&')
    all_programs = []
    all_program_names = []
    cur_index = 0
    while True:
        start_index = page_source.find('f=', cur_index) + 2
        if (start_index - 2) == -1:
            break
        end_index = page_source.find('>', start_index)
        content = page_source[start_index : end_index].strip('"')
        if content not in all_programs:
            all_programs.append(content)
            if calendar:
                end_of_name = page_source.find('<', end_index)
                program_name = page_source[end_index + 1 : end_of_name]
                all_program_names.append(program_name.strip())

        cur_index = end_index

    return (all_programs, all_program_names)




calendar_source = \
'''
<li>
<a href="199299398399.html">199/299/398/399</a>
</li>
<li>
<a href="crs_abs.htm">Aboriginal Studies</a>
</li>
<li>
<a href="crs_act.htm">Actuarial Science</a>
</li>
<li>
<a href="crs_usa.htm">American Studies</a>
</li>
<li>
<a href="crs_ana.htm">Anatomy</a>
</li>
<li>
<a href="crs_ant.htm">Anthropology</a>
</li>
<li>
<a href="crs_arc.htm">Architecture</a>
</li>
<li>
<a href="crs_arh.htm">Archaeology</a>
</li>
<li>
<a href="crs_fah.htm">Art</a>
</li>
<li>
<a href="crs_asi.htm">Asia-Pacific Studies</a>
</li>
<li>
<a href="crs_asi.htm">Asian Studies, Contemporary</a>
</li>
<li>
<a href="crs_ast.htm">Astronomy and Astrophysics</a>
</li>
<li>
<a href="crs_bch.htm">Biochemistry</a>
</li>
<li>
<a href="crs_bio.htm">Biology</a>
</li>
<li>
<a href="Academic_Bridging_Program.html">Academic Bridging Program</a>
</li>
<li>
<a href="crs_cta.htm">Canadian Institute for Theoretical Astrophysics </a>
</li>
<li>
<a href="crs_chm.htm">Chemistry</a>
</li>
<li>
<a href="crs_cla.htm">Classics</a>
</li>
<li>
<a href="crs_cog.htm">Cognitive Science</a>
</li>
<li>
<a href="crs_col.htm">Comparative Literature</a>
</li>
<li>
<a href="crs_csb.htm">Cell and Systems Biology</a>
</li>
<li>
<a href="crs_csc.htm">Computer Science</a>
</li>
<li>
<a href="crs_drm.htm">Drama</a>
</li>
<li>
<a href="crs_dts.htm">Diaspora and Transnational Studies</a>
</li>
<li>
<a href="crs_eas.htm">East Asian Studies</a>
</li>
<li>
<a href="crs_eco.htm">Economics</a>
</li>
<li>
<a href="crs_eeb.htm">Ecology and Evolutionary Biology</a>
</li>
<li>
<a href="crs_eng.htm">English</a>
</li>
<li>
<a href="crs_eth.htm">Ethics (Centre for)</a>
</li>
<li>
<a href="crs_env.htm">Centre for Environment</a>
</li>
<li>
<a href="crs_est.htm">Estonian</a>
</li>
<li>
<a href="crs_eur.htm">European Studies</a>
</li>
<li>
<a href="crs_fin.htm">Finnish</a>
</li>
<li>
<a href="crs_for.htm">Forest Conservation</a>
</li>
<li>
<a href="crs_fre.htm">French</a>
</li>
<li>
<a href="crs_ger.htm">German</a>
</li>
<li>
<a href="crs_ggr.htm">Geography</a>
</li>
<li>
<a href="crs_glg.htm">Geology </a>
</li>
<li>
<a href="crs_his.htm">History</a>
</li>
<li>
<a href="crs_hmb.htm">Human Biology</a>
</li>
<li>
<a href="crs_hps.htm">History and Philosophy of Science and Technology</a>
</li>
<li>
<a href="crs_hun.htm">Hungarian</a>
</li>
<li>
<a href="crs_imm.htm">Immunology</a>
</li>
<li>
<a href="crs_ini.htm">Innis College</a>
</li>
<li>
<a href="crs_ita.htm">Italian</a>
</li>
<li>
<a href="crs_cjs.htm">Centre for Jewish Studies</a>
</li>
<li>
<a href="crs_jxx.htm">Joint Courses</a>
</li>
<li>
<a href="crs_phe.htm">Kinesiology &amp; Physical Education</a>
</li>
<li>
<a href="crs_las.htm">Latin American Studies</a>
</li>
<li>
<a href="Life_Sciences.html">Life Sciences</a>
</li>
<li>
<a href="crs_lin.htm">Linguistics</a>
</li>
<li>
<a href="crs_lmp.htm">Laboratory Medicine and Pathobiology</a>
</li>
<li>
<a href="crs_mat.htm">Mathematics</a>
</li>
<li>
<a href="crs_mll.htm">Modern Languages and Literatures</a>
</li>
<li>
<a href="crs_mgy.htm">Molecular Genetics and Microbiology</a>
</li>
<li>
<a href="crs_mse.htm">Materials Science</a>
</li>
<li>
<a href="crs_mus.htm">Music</a>
</li>
<li>
<a href="crs_new.htm">New College</a>
</li>
<li>
<a href="crs_nfs.htm">Nutritional Science</a>
</li>
<li>
<a href="crs_nmc.htm">Near and Middle Eastern Civilizations</a>
</li>
<li>
<a href="crs_pcl.htm">Pharmacology and Toxicology</a>
</li>
<li>
<a href="crs_pcs.htm">Peace, Conflict and Justice Studies</a>
</li>
<li>
<a href="crs_phc.htm">Pharmaceutical Chemistry</a>
</li>
<li>
<a href="crs_phl.htm">Philosophy</a>
</li>
<li>
<a href="crs_phy.htm">Physics</a>
</li>
<li>
<a href="crs_pln.htm">Planetary Science</a>
</li>
<li>
<a href="crs_pol.htm">Political Science</a>
</li>
<li>
<a href="crs_prt.htm">Portuguese</a>
</li>
<li>
<a href="crs_psl.htm">Physiology</a>
</li>
<li>
<a href="crs_psy.htm">Psychology</a>
</li>
<li>
<a href="crs_phs.htm">Public Health Sciences</a>
</li>
<li>
<a href="crs_ppg.htm">Public Policy </a>
</li>
<li>
<a href="crs_rlg.htm">Religion</a>
</li>
<li>
<a href="crs_rsm.htm">Rotman Commerce</a>
</li>
<li>
<a href="crs_sla.htm">Slavic Languages and Literatures</a>
</li>
<li>
<a href="crs_smc.htm">St. Michael's College</a>
</li>
<li>
<a href="crs_soc.htm">Sociology</a>
</li>
<li>
<a href="crs_sas.htm">South Asian Studies</a>
</li>
<li>
<a href="crs_spa.htm">Spanish</a>
</li>
<li>
<a href="crs_sta.htm">Statistics</a>
</li>
<li>
<a href="crs_trn.htm">Trinity College</a>
</li>
<li>
<a href="crs_uni.htm">University College</a>
</li>
<li>
<a href="crs_vic.htm">Victoria College</a>
</li>
<li>
<a href="crs_wdw.htm">Woodsworth College</a>
</li>
<li>
<a href="crs_wgs.htm">Women and Gender Studies</a>
</li>

'''



timetable_source = \
'''
<li><a href="asabs.html">Aboriginal
    Studies [ABS courses - includes JFP450H1]</a>
<li><a href="wdw.html">Academic Bridging Program [ENG185Y1,
JWH100Y1 and JWU100Y1] </a>
<li><a href="stat.html">Actuarial Science [ACT
    courses]</a>
<li><a href=csus.html>American Studies [USA courses]</a>
<li><a href=ana.html>Anatomy [ANA courses]</a>
<li><a href=ant.html>Anthropology
    [ANT courses - includes ARH]</a>
<li><a href="mat.html">Applied Mathematics [APM
    courses]</a>
<li><a href="ant.html">Archaeology [ARH courses]</a>
<li><a href=arcla.html>Architecture [ARC courses]</a>
<li><a href="far.html">Art
- Art History Courses [FAH courses] </a>
<li><a href="far.html"> Art - Visual Studies Courses [VIS
  courses]</a><li><a href=ast.html>Astronomy
    [AST courses - includes PLN]</a>

<li><a href=bch.html>Biochemistry [BCH courses - includes
    BCB]</a>
<li>Biology [for <a href="csb.html">BIO130H1,
    230H1,
255H1,  260H1, 270H1 and 271H1 see CSB;</a> for <a href="eeb.html">BIO120H1, 220H1 and 251H1 see EEB]</a>
<li><a href="cita.html">Canadian Institute for Theoretical Astronomy [CTA courses]</a>
<li><a href=chm.html>Chemistry [CHM courses - includes JSC310H1]</a>
<li><a href="cfe.html">Centre
for Environment [ENV courses</a> - for ENV234H1, 334H1 see <a href="eeb.html">EEB</a>; for ENV315H1 see <a href="glg.html">GLG</a>; for JEH455H1 see <a href="hmb.html">HMB</a>; for ENV235H1 see <a href="phy.html">PHY</a> <a href="phy.html">]</a>

<li><a href="ethic.html">Centre for Ethics [ETH courses]</a>
<li><a href="cjs.html">Centre for Jewish Studies [CJS courses]</a><li><a href=col.html>Centre for Comparative Literature [COL courses]</a>
<li><a href=csb.html>Cell
    and Systems Biology [CSB courses - includes BIO130H1, 230H1, 255H1,
     260H1, 270H1 and 271H1]</a>
<li><a href="clas.html">Classics [CLA courses - includes GRK, and LAT]</a>
<li><a href="phl.html">Cognitive Science [COG courses]</a>
<li><a href=csc.html>Computer Science [CSC courses - includes ECE]</a>
<li><a href="asi.html">Contemporary Asian Studies [CAS courses]</a>
<li><a href="dts.html">Diaspora and Transnational Studies [DTS courses]</a>
<li><a href=uc.html>Drama [DRM courses]</a><li><a href=eas.html>East Asian Studies [EAS courses]</a>
<li><a href="eeb.html">Ecology &amp; Evolutionary
    Biology [EEB courses - includes BIO120H1, 220H1, 251H1, EHJ352H1, ENV234H1, 334H1
and JMB170Y1]</a>
<li><a href=eco.html>Economics [ECO courses]</a>
<li><a href="new.html">English Language Learning
[ELL courses]</a>
<li><a href=eng.html>English
    [ENG courses - includes JEI206H1]</a>
<li><a href=sla.html>Estonian [EST courses]</a>
<li><a href=ceres.html>European Studies [EUR courses]</a>
<li><a href="sla.html">Finnish
    [FIN courses]</a>
<li><a href="artsc.html">First Year Learning Community
    [ACT099Y1, CSC099Y1, ECO099Y1, FLC099Y1, INI099Y1, NEW099Y1, PHL099Y1, PSY099Y1, RSM099Y1, SMC099Y1, TRN099Y1, UNI099Y1, VIC099Y1, WDW099Y1 courses] </a>
<li><a href="assem.html">First Year Seminars [CCR199H1, CCR199Y1, LTE199H1, LTE199Y1, PMU199H1, PMU199Y1, SII199H1, SII199Y1, TBB199H1, TBB199Y1, XBC199Y1]</a>
<li><a href=for.html>Forestry [FOR courses]</a>
<li><a href=fre.html>French
    [FRE courses - includes FCS, FSL, JFI255Y1 and JFL477H1]</a>
<li><a href=ger.html>German [GER courses]</a>
<li><a href=ggr.html>Geography
    [GGR courses - includes  JFG475H1, JGE236H1, 321H1, 331H1 and JGI216H1, 346H1, 454H1]</a>
<li><a href=glg.html>Geology [GLG courses - includes ENV315H1]</a>
<li><a href="clas.html">Greek [GRK courses]</a>

<li><a href="his.html">History
    [HIS courses </a><a href="his.html">- includes JHA394H1,</a> for JHP see <a href="pol.html">POL</a>]
<li><a href=hmb.html>Human
    Biology [HMB courses - includes HAJ453H1 and JEH455H1]</a>
<li><a href="hun.html">Hungarian [HUN courses]</a>
<li><a href="imm.html">Immunology [IMM courses]</a>
<li><a href=ihpst.html>Institute of History And Philsophy
    Of Science [HPS courses - includes JHE353H1 and JPH311H1]</a>
<li><a href="innis.html">Innis College Courses [INI
    courses - includes IJC400H1,</a> for JGI216H1 see <a href="ggr.html">GGR</a>]
<li><a href=ita.html>Italian [ITA courses]</a>
<li><a href="lmp.html">Laboratory Medicine and Pathobiology [LMP courses]</a>
<li><a href="clas.html">Latin [LAT courses]</a>

<li><a href=las.html>Latin American Studies [LAS courses]</a>
<li><a href="lin.html">Linguistics
    [LIN courses - includes JAL353H1 401H1, JLP315H1, 374H1, 471H1 and JLS474H1</a>]
<li><a href=mat.html>Mathematics [MAT courses - includes APM]</a>
<li><a href="rlg.html">Modern Hebrew [MHB courses]</a>
<li><a href=medgm.html>Molecular Genetics and Microbiology [MGY courses - includes MIJ485H1]</a>
<li><a href=music.html>Music [MUS courses]</a>

<li><a href="nmc.html">Near &amp; Middle Eastern Civilizations [NMC courses - includes NML]</a>
<li><a href=new.html>New College Courses [NEW courses
    - includes ELL, IFP, JNH350H1, JQR360H1]</a>
<li><a href="nusci.html">Nutritional Science [NFS courses]</a>
<li><a href="glaf.html">Peace, Conflict and Justice Studies [PCJ courses]</a>
<li><a href="phm.html">Pharmaceutical Chemistry [PHC
courses]</a>
<li><a href=pcl.html>Pharmacology [PCL courses]</a>
<li><a href=phl.html>Philosophy [PHL courses - includes COG]</a>
<li><a href=phy.html>Physics [PHY courses - includes
    ENV235H1,  JOP210H1 and JPH441H1]</a>

<li><a href="psl.html">Physiology [PSL courses]</a>
<li><a href="ast.html">Planetary Science [PLN
    courses]</a>
<li><a href="pol.html">Political
Science [POL courses - includes JHP304Y1, JPA308H1, 331Y1, 411H1, 462H1, JPF455Y1, JPR364Y1, 374H1 and JPU315H1]</a>
<li><a href="spa.html">Portuguese [PRT courses]</a>
<li><a href="psy.html">Psychology [PSY courses]</a>
<li><a href="uc.html">Public Health Science [PHS courses]</a>
<li><a href=rlg.html>Religion [RLG courses - includes JPR419H1, 457H1
    and MHB]</a>
<li><a href="compg.html">Rotman
    Commerce
[RSM courses - includes MGT201H1]</a>
<li><a href="smc.html">St. Michael's College Courses [SMC
courses - </a>for JSV200H1 see <a href="vic.html">VIC] </a>
<li><a href=sla.html>Slavic Languages And Literature [SLA
    courses - includes EST and FIN]</a><li><a href="soc.html">Sociology [SOC courses]</a>
<li><a href="sas.html">South Asian Studies [SAS courses]</a>
<li><a href=spa.html>Spanish [SPA courses - includes PRT]</a>
<li><a href=stat.html>Statistics [STA courses - includes ACT]</a>
<li><a href=trin.html>Trinity College Courses [TRN courses]</a>
<li><a href=uc.html>University
    College Courses [UNI courses - includes DRM, JDC400Y1,  410H1, JUM205H1 and PHS]</a>
<li><a href=vic.html>Victoria College Courses [VIC courses
    </a> <a href="vic.html">includes JSV200H1]</a>
<li><a href=wdw.html>Woodsworth College Courses [WDW courses
    - includes  Academic Bridging Program (ENG185Y1, JWH100Y1 and
    JWU100Y1)]</a>
<li><a href=wgsi.html>Women and Gender Studies [WGS courses]</a>'''


if __name__ == "__main__":
    find_urls(True)
    
