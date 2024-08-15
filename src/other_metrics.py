import numpy as np
#*Funcion para calcular AP por cada usuario, al final la sumatoria de todos los AP entre la cantidad de usuarios da la 
#*métrica de MAP

#* getPropertyFunc: una lambda funcion que obtenga de los elementos del array la propiedad segun la cual se puede saber si 
#* el elemento es un hit


#*isHitFunc: lambda funcion que dira si es un hit 

def average_prediction(predicted_ratings,isHitFunc, getPropertyFunc):
    rel=0
    numerator=0
    for index,rating in enumerate(predicted_ratings):
        if(isHitFunc(getPropertyFunc(rating))):
            rel+=1
            ##print((rel/(index+1)))
            numerator+=(rel/(index+1))
    if(rel>0):
        return (numerator/rel)
    else:
        return 0


# hits=[0,1,0,1,1]
# print(average_prediction(hits,lambda x: x==1))
            