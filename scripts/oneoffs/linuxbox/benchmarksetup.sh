echo 0 | sudo tee randomize_va_space
echo "never" | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
echo "never" | sudo tee /sys/kernel/mm/transparent_hugepage/defrag
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

#Set minimum frequency to maximum frequency
echo 3900000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq

# Turn of hyperthreaded cores
echo 0  | sudo tee cpu7/online
echo 0  | sudo tee cpu8/online
echo 0  | sudo tee cpu9/online
echo 0  | sudo tee cpu10/online
echo 0  | sudo tee cpu11/online
