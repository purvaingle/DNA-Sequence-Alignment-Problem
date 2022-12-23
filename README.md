# DNA-Sequence-Alignment-Problem
Please find the detailed description of the problem statement [here](https://github.com/purvaingle/DNA-Sequence-Alignment-Problem/blob/main/CSCI570_Fall22_Project.pdf)

Summary of the results
![Test Image 1](https://github.com/purvaingle/DNA-Sequence-Alignment-Problem/blob/main/Screen%20Shot%202022-12-22%20at%206.52.21%20PM.png?raw=true)


## Graph1 – Memory vs Problem Size (M+N)
<img width="505" alt="Screen Shot 2022-12-22 at 6 56 33 PM" src="https://user-images.githubusercontent.com/90026828/209261791-a6e3d092-f184-4a76-a7fe-9f4e20f1cc45.png">

Nature of the Graph (Logarithmic/ Linear/ Polynomial/ Exponential)
Basic: Linear
Efficient: Polynomial (Quadratic)
Explanation: The memory efficient algorithm only consumes a linear amount of memory because it does not need to store the whole dynamic programming table of optimal alignments – it only needs to store two columns: the current column and the previous column.


## Graph2 – Time vs Problem Size (M+N)
<img width="547" alt="Screen Shot 2022-12-22 at 6 58 06 PM" src="https://user-images.githubusercontent.com/90026828/209261993-14680524-6a77-4d9b-a055-80b7917391d2.png">

Nature of the Graph (Logarithmic/ Linear/ Polynomial/ Exponential)
Basic: Polynomial Efficient: Polynomial
Explanation: The memory efficient algorithm takes twice as long as the basic algorithm, since it performs Cmn work at the root level, and Cmn/2 at the next level, and so on, which sums up to 2Cmn = O(mn). The basic algorithm simply uses dynamic programming, and there are mn unique subproblems, hence the runtime O(mn).
