## IBM Model 1
Martino Ferrari
### Exercise 1
The simple IBM1 model is implemented in the ```ibm1.py``` that permits to compute
the translation probability of a given sentence.

To execute the exercise run ```e1.py``` script with argument ```e1.json``` that
contain the specified parameters.  

The results for the given example are the following:

**F: das Haus ist klein   
E: the house is small**   
  Best aligment: (0, 1, 2, 3)   
  Aligment probability: 0.00028672   
  Translation probability: 0.00028672   

**F: das Haus ist klein    
E: the house is little**    
  Best aligment: (0, 1, 2, 3)   
  Aligment probability: 0.00028672   
  Translation probability: 0.00028672   

**F: das Haus ist klein    
E: small house the is**   
  Best aligment: (2, 1, 3, 0)   
  Aligment probability: 0.00028672   
  Translation probability: 0.00028672   

**F: das Haus ist klein   
E: the**   
  Best aligment: (0, 0, 0, 0)   
  Aligment probability: 0.0   
  Translation probability: 0.0   



### Exercise 2

To execute the exercise run ```e2.py``` script with argument ```e2.json```

After adapting the previously implemented EM algorithm for the IBM model 1, I used it over the given data, the EM converged after 4 iterations with the following results:

- la :
  + blue : 0.0
  + the : 0.5024228309069763
  + house : 0.4975771690930237
- bleue :
  + blue : 0.5024228309069763
  + the : 0.0
  + house : 0.4975771690930237
- maison :
  + blue : 0.24997659100159095
  + the : 0.24997659100159095
  + house : 0.5000468179968182


While using 1 as alignment probability q(..) the result after 4 iteration is:

- la :
  + blue : 0.0
  + the : 0.523484442144212
  + house : 0.47651555785578803
- maison :
  + blue : 0.24789970591317362
  + the : 0.24789970591317362
  + house : 0.5042005881736529
- bleue :
  + blue : 0.523484442144212
  + the : 0.0
  + house : 0.47651555785578814
