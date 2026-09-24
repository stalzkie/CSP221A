The averages and flags in this program are vectorized because NumPy handles the values in the array all at once instead of checking each robot using a separate loop. For example, 'mean(axis=1)' gets the average cycle time for every robot, while 'np.where()' checks which cycle times are above the limit. The normalization also works on whole columns using broadcasting. If I used regular loops inside these methods, the code would be longer and would not fully take advantage of NumPy.



output:
Average Cycle Times:
Robot: R-01, Average Cycle Time: 42.90 min average
Robot: R-02, Average Cycle Time: 49.57 min average
Robot: R-05, Average Cycle Time: 44.40 min average
Robot: R-06, Average Cycle Time: 55.37 min average

Longest Cycle:
Robot: R-01, Longest Cycle: 45.50
Robot: R-02, Longest Cycle: 50.10
Robot: R-05, Longest Cycle: 45.00
Robot: R-06, Longest Cycle: 56.10

Cycle Flags:
Robot: R-01, Cycle Flag: ['NORMAL' 'SLOW_CHARGE' 'NORMAL']
Robot: R-02, Cycle Flag: ['SLOW_CHARGE' 'SLOW_CHARGE' 'SLOW_CHARGE']
Robot: R-05, Cycle Flag: ['NORMAL' 'NORMAL' 'NORMAL']
Robot: R-06, Cycle Flag: ['SLOW_CHARGE' 'SLOW_CHARGE' 'SLOW_CHARGE']

Normalized Columns:
[[-1.15541043 -0.64331317 -1.22806998]
 [ 0.42413801  0.11913207  0.33166854]
 [-0.68739608 -1.0483622  -0.54680488]
 [ 1.4186685   1.5725433   1.44320633]]