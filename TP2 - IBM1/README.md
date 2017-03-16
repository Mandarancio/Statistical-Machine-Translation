## IBM Model 1
Martino Ferrari
### Exercise 1
The simple IBM1 model is implemented in the ```ibm1.py``` that permits to compute
the translation probability of a given sentence.

To execute the exercise run ```e1.py``` script with argument ```e1.json``` that
contain the specified parameters.  

The results for the given example are the following:

**E: das Haus ist klein   
F: the house is small   **

Best aligment: (0, 1, 2, 3)   
Aligment probability: 0.00028672   
Translation probability: 0.00028672   

**E: das Haus ist klein   
F: the house is little**

Best aligment: (0, 1, 2, 3)   
Aligment probability: 0.00028672  
Translation probability: 0.00028672  

**E: das Haus ist klein   
F: small house the is**

Best aligment: (3, 1, 0, 2)  
Aligment probability: 0.0002867200000000001  
Translation probability: 0.0002867200000000001  

**E: das Haus ist klein   
F: the**

Best aligment: (0,)   
Aligment probability: 0.13999999999999999   
Translation probability: 0.13999999999999999   


### Exercise 2

To execute the exercise run ```e2.py``` script with argument ```e2.json```

After adapting the previously implemented EM algorithm for the IBM model 1, I used it over the given datas. After 5 iterations it converged (the convergency condition is an epsilon=1e-5) with the following results:

- bleue :
  + house : 0.4975656836219058
  + blue : 0.5024343163780942
  + the : 0.0
- maison :
  + house : 0.5037212936707866
  + blue : 0.25054871388179895
  + the : 0.24572999244741456
- la :
  + house : 0.5024815799620439
  + blue : 0.0
  + the : 0.49751842003795604
