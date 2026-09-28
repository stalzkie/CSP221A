By making athlete names and times a Numpy array, we can perform vectorized calls on it. Vectorized functions performs operations on the whole array at once instead of looping through each item in the array, which is slow in dynamically types languages like Python since it has to determine the data type for every loop. This is possible by storing the items close together in the memory block. Averages/flags count are vectorized functions because we do not loop through each item but perform the operation at once on the times array.

Things could break if:
- times Numpy array has different shapes (which is why we validated raw_rows in the first place)
- setting wrong data type in numpy array constructor will break your data (inserting float data into int numpy array will perform narrowing conversion on float data)
