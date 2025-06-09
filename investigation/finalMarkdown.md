**step 1**: Mark all vertex as unvisited
![](2.jpg)
unvisited_vertex:
['A', 'B', 'C', 'D', 'E', 'F', 'G']

| vertex | distance from start | previous vertex |
| ------ | ------------------- | --------------- |
| A | inf | None |
| B | inf | None |
| C | inf | None |
| D | inf | None |
| E | inf | None |
| F | inf | None |
| G | inf | None |


**step 2**: Mark all other nodes to infinity
![](3.jpg)
unvisited_vertex:
['A', 'B', 'C', 'D', 'E', 'F', 'G']

| vertex | distance from start | previous vertex |
| ------ | ------------------- | --------------- |
| A | 0 | None |
| B | inf | None |
| C | inf | None |
| D | inf | None |
| E | inf | None |
| F | inf | None |
| G | inf | None |


**step 3**: start a while loop

**step 3a**: For the current node, calculate all unvisited neighbors. Place the previous node on it.

**step 3b**: Update the shortest distance, if new distance is shorter

**step 3c**: Mark current node as visited
![](4.jpg)
unvisited_vertex:
['B', 'C', 'D', 'E', 'F', 'G']

| vertex | distance from start | previous vertex |
| ------ | ------------------- | --------------- |
| A | 0 | None |
| B | 5 | A |
| C | inf | None |
| D | 7 | A |
| E | 20 | A |
| F | inf | None |
| G | inf | None |


![](5.jpg)
unvisited_vertex:
['C', 'D', 'E', 'F', 'G']

| vertex | distance from start | previous vertex |
| ------ | ------------------- | --------------- |
| A | 0 | None |
| B | 5 | A |
| C | inf | None |
| D | 7 | A |
| E | 8 | B |
| F | inf | None |
| G | inf | None |


![](6.jpg)
unvisited_vertex:
['C', 'E', 'F', 'G']

| vertex | distance from start | previous vertex |
| ------ | ------------------- | --------------- |
| A | 0 | None |
| B | 5 | A |
| C | inf | None |
| D | 7 | A |
| E | 8 | B |
| F | inf | None |
| G | inf | None |


![](7.jpg)
unvisited_vertex:
['C', 'F', 'G']

| vertex | distance from start | previous vertex |
| ------ | ------------------- | --------------- |
| A | 0 | None |
| B | 5 | A |
| C | inf | None |
| D | 7 | A |
| E | 8 | B |
| F | 13 | E |
| G | 14 | E |


![](8.jpg)
unvisited_vertex:
['C', 'G']

| vertex | distance from start | previous vertex |
| ------ | ------------------- | --------------- |
| A | 0 | None |
| B | 5 | A |
| C | 15 | F |
| D | 7 | A |
| E | 8 | B |
| F | 13 | E |
| G | 14 | E |


![](9.jpg)
unvisited_vertex:
['C']

| vertex | distance from start | previous vertex |
| ------ | ------------------- | --------------- |
| A | 0 | None |
| B | 5 | A |
| C | 15 | F |
| D | 7 | A |
| E | 8 | B |
| F | 13 | E |
| G | 14 | E |


![](10.jpg)
unvisited_vertex:
[]

| vertex | distance from start | previous vertex |
| ------ | ------------------- | --------------- |
| A | 0 | None |
| B | 5 | A |
| C | 15 | F |
| D | 7 | A |
| E | 8 | B |
| F | 13 | E |
| G | 14 | E |


**step 5**: after there are no unvisited_node, calculate the paths

**step 5a**: the path are calculated by tracing back the previous node
![](final.jpg)
