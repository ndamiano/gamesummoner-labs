"""Record batch windows with the doorbell graph even when every expert is resident: the batch host loop waits for doorbells."""
import sys
p = sys.argv[1] + "/src/core/verify.cpp"
s = open(p).read()
old = "    row_base_ = hbase;\n    std::string rerr;\n    const bool ok = record_window(R, cs_, rerr);\n    batch_rec_ = false;\n"
new = ("    row_base_ = hbase;\n    std::string rerr;\n    const bool ar_save = ar_off_;\n    ar_off_ = true;\n"
       "    const bool ok = record_window(R, cs_, rerr);\n    ar_off_ = ar_save;\n    batch_rec_ = false;\n")
assert s.count(old) == 1, s.count(old)
open(p, "w").write(s.replace(old, new))
print("patched")
