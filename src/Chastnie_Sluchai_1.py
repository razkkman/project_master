def Chastnie_Sluchai_1_(array_next, array_now, A):
    S = 0
    
    #1
        
    if ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += A**2 
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (7*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (7*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (7*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (7*A**2)/8
        

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += A**2 
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (7*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (7*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (7*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (7*A**2)/8

    #2
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += (A**2)/2

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += (A**2)/2

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += (A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += (A**2)/4
        

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += (A**2)/2

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += (A**2)/2

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += (A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += (A**2)/4

    #3

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111"):                
        S += (A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011"):                
        S += (A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101"):                
        S += (A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110"):                
        S += (A**2)/8
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111"):                
        S += (A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011"):                
        S += (A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101"):                
        S += (A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110"):                
        S += (A**2)/8
        
        
    #1110,1101,1011,0111
        
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (7*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (7*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (7*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (7*A**2)/8
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (7*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (7*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (7*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (7*A**2)/8
        
        
    #1100...
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (A**2)/2

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (A**2)/2

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (3*A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (3*A**2)/4
        

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (A**2)/2

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (A**2)/2

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (3*A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (3*A**2)/4
        
        
    #1000...
    
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0000"):                
        S += (A**2)/8
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0000"):                
        S += (A**2)/8
        
        
    #1110...1000
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += A**2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (3*A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (3*A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (3*A**2)/4
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += A**2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (3*A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (3*A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (3*A**2)/4
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (3*A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (3*A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (3*A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += A**2
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (3*A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (3*A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (3*A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += A**2
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (3*A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (3*A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += A**2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (3*A**2)/4
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (3*A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (3*A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += A**2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (3*A**2)/4
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (3*A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += A**2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (3*A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (3*A**2)/4
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (3*A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += A**2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (3*A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (3*A**2)/4
        
    #%%
    #1110...1100
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += (3*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += (3*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += (5*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += (5*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += (A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += (3*A**2)/8
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += (3*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += (3*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += (5*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += (5*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += (A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += (3*A**2)/8
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += (3*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += (5*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += (5*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += (3*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += (3*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += (A**2)/8
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += (3*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += (5*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += (5*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += (3*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += (3*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += (A**2)/8
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += (5*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += (3*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += (3*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += (5*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += (3*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += (A**2)/8
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += (5*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += (3*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += (3*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += (5*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += (3*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += (A**2)/8
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += (5*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += (5*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += (3*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += (3*A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += (A**2)/8
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += (3*A**2)/8
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += (5*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += (5*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += (3*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += (3*A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += (A**2)/8
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += (3*A**2)/8
        
    #%%
    #1110...1110
        
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111"):                
        S += (A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011"):                
        S += (A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101"):                
        S += 0
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110"):                
        S += (A**2)/4
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111"):                
        S += (A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011"):                
        S += (A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101"):                
        S += 0
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110"):                
        S += (A**2)/4
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111"):                
        S += (A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011"):                
        S += (A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101"):                
        S += (A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110"):                
        S += 0
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111"):                
        S += (A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011"):                
        S += (A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101"):                
        S += (A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110"):                
        S += 0
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111"):                
        S += 0
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011"):                
        S += (A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101"):                
        S += (A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110"):                
        S += (A**2)/4
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111"):                
        S += 0
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011"):                
        S += (A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101"):                
        S += (A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110"):                
        S += (A**2)/4
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111"):                
        S += (A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1011"):                
        S += 0
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1101"):                
        S += (A**2)/4
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1110"):                
        S += (A**2)/4
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0111"):                
        S += (A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1011"):                
        S += 0
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1101"):                
        S += (A**2)/4
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0111" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1110"):                
        S += (A**2)/4
        
        
    #%%
    #1100...1000
        
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (3*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (3*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (5*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (5*A**2)/8
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (3*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (3*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (5*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (5*A**2)/8
        
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (5*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (7*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (7*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (5*A**2)/8
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (5*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (7*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (7*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (5*A**2)/8
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (5*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (5*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (3*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (3*A**2)/8
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (5*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (5*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (3*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (3*A**2)/8
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (7*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (5*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (5*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (7*A**2)/8
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (7*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (5*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (5*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (7*A**2)/8
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (5*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (3*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (5*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (3*A**2)/8
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (5*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (3*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (5*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (3*A**2)/8
    
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (3*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (5*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (3*A**2)/8

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (5*A**2)/8
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (3*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (5*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (3*A**2)/8

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (5*A**2)/8
        
    #%%
    #1100...1100
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += 0
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += (A**2)
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += (A**2)/2
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += 0
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += (A**2)
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += (A**2)/2
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += 0
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += (A**2)/2
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += 0
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += (A**2)/2
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += (A**2)
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += 0
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += (A**2)/2
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += (A**2)
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += 0
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += (A**2)/2
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += 0
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += 0
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += 0
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += (A**2)
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += (A**2)/2
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += 0
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += (A**2)
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += (A**2)/2
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1100"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101"):                
        S += (A**2)
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0011"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1010"):                
        S += 0
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1001"):                
        S += (A**2)/2
        
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0110"):                
        S += (A**2)/2
    
    
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1100"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0101"):                
        S += (A**2)
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0011"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1010"):                
        S += 0
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1001"):                
        S += (A**2)/2
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0101" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0110"):                
        S += (A**2)/2
        
        
    #%%
    #1000...1000
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += 0

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (A**2)/4
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += 0

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (A**2)/4
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += 0

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (A**2)/4
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += 0

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (A**2)/4
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += (A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += 0
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += (A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += 0
    
    
    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "1000"):                
        S += (A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0100"):                
        S += (A**2)/4

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0010"):                
        S += 0

    elif ((array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001" and (array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001"):                
        S += (A**2)/4
        
        
    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "1000"):                
        S += (A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0100"):                
        S += (A**2)/4

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0010"):                
        S += 0

    elif ((array_next[0]+array_next[1]+array_next[4]+array_next[5]) == "0001" and (array_now[2]+array_now[3]+array_now[6]+array_now[7]) == "0001"):                
        S += (A**2)/4
           
    return S
