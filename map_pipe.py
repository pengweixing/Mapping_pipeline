#################################################
#  File Name:map_pipe.py
#  Author: xingpengwei
#  Mail: xingwei421@qq.com,pengwei.xing@igp.uu.se,xpw1992@gmail.com
#  Created Time: Fri Jan 14 11:32:37 2022
#################################################
## sample list
"""
sample_name1 *L1_R1.fq.gz *L1_R2.fq.gz
sample_name1 *L2_R1.fq.gz *L2_R2.fq.gz
sample_name2 *L1_R1.fq.gz *L1_R2.fq.gz
sample_name2 *L2_R1.fq.gz *L2_R2.fq.gz
"""
import sys,os

f_list = open(sys.argv[1],'r')## sample list
f_map = open("run_map.sh",'w')
all_list = [line.strip() for line in f_list.readlines()]
name = ''
last=all_list[0].split()[0]
for line in all_list:
    line = line.strip()
    line1 = line.split('\t')
    out = line1[0]
    R1 = line1[1]
    R2 = line1[2]
    if out == name:
        mapping_cmd = "bwa mem -t 30  -R '@RG\\tID:foo\\tSM:{sam_name}\\tLB:library1' /disk1/pengweixing/database/CHM13/chm13v2.0.fa " \
            + R1 + " " + R2 + " |samtools view -@ 10 - -b |samtools sort -m 10G -@ 10 - -o  ./{sam_name}/{outname}.sort.bam" 
        f_map.write("%s\n" % mapping_cmd.format(sam_name=line1[0],outname=out))
    else:
        if not name == '':
            merge_cmd = "ls ./{sam_name}/*sort.bam > ./{sam_name}/bam.list\nsamtools merge -@ 10 -b ./{sam_name}/bam.list ./{sam_name}/{sam_name}.merge.sort.bam\ncat ./{sam_name}/bam.list|xargs rm"
            mark_dup_cmd = "java -Xmx4G -jar /disk1/pengweixing/software/picard.jar MarkDuplicates --INPUT ./{sam_name}/{sam_name}.merge.sort.bam --METRICS_FILE ./{sam_name}/{sam_name}.sort.matrix --OUTPUT ./{sam_name}/{sam_name}.mardup.sort.bam > ./{sam_name}/{sam_name}.picar.log"
            f_map.write("%s\n" % merge_cmd.format(sam_name=last))
            f_map.write("%s\n" % mark_dup_cmd.format(sam_name=last))
            f_map.write("rm %s.merge.sort.bam \n" % last)
        dir_cmd = "mkdir " + out
        mapping_cmd = "bwa mem -t 30  -R '@RG\\tID:foo\\tSM:{sam_name}\\tLB:library1' /disk1/pengweixing/database/CHM13/chm13v2.0.fa " \
                    + line1[1] + " " + line1[2] + " |samtools view -@ 10 - -b |samtools sort -m 10G -@ 10 - -o  ./{sam_name}/{sam_name}.sort.bam" 
        f_map.write("%s\n" % dir_cmd)
        f_map.write("%s\n" % mapping_cmd.format(sam_name=out))
        last = out
        name = out
