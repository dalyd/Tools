# Disable hypethreading (nj specific)
echo 0 > /sys/devices/system/cpu/cpu8/online
echo 0 > /sys/devices/system/cpu/cpu9/online
echo 0 > /sys/devices/system/cpu/cpu10/online
echo 0 > /sys/devices/system/cpu/cpu11/online
echo 0 > /sys/devices/system/cpu/cpu12/online
echo 0 > /sys/devices/system/cpu/cpu13/online
echo 0 > /sys/devices/system/cpu/cpu14/online
echo 0 > /sys/devices/system/cpu/cpu15/online

# disable ASLR (Address Space Layout Randomization)
echo 0 > /proc/sys/kernel/randomize_va_space
# disable transparent huge pages
echo "never" > /sys/kernel/mm/transparent_hugepage/enabled
echo "never" > /sys/kernel/mm/transparent_hugepage/defrag
# if cpufreq scaling governor is present, ensure we aren't in power save (speed step) mode
if [ -e /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor ]
then
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
fi
