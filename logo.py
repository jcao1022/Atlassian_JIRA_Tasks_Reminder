


def cafe_logo(v, sv, sv2=0):

    logo = '''
    
    \033[1;34;40m

            0000000                                                                                                     
         000000             00000                                                                                       
      00000000            0000000000                                                                                    
    00000000           000000000000000                           00            00                                       
   000000000         00000000000000000000                       0  0          0  0                                      
  0000000000000         0000000000000                             000         000                                       
 000000000     0000     0000000000000       00000000000000000    0000000000000000   00000000000000000 00000000000000000 
 000000000              0000000000000      000000000000000000   000000000000000000  00000000000000000 0000000000000000  
0000000000              0000000000000      0000                 000  0 0  0 0  000  0000              000               
0000000000              0000000000000      0000                 000  000  000  000  0000              000               
0000000000000000000     0000000000000      0000                 000000000000000000  00000000000000    00000000000000    
0000000000              0000000000000      0000                 000000000000000000  0000              000               
0000000000                                 0000                 000            000  0000              000               
0000000000                 0000000         0000                 000            000  0000              000               
 000000000                 000000           00000000000000000   000            000  0000              00000000000000000 
  00000000000000000        00000                                                                                        
   00000000               00000                                                                                         
    00000000             00000                                                                    Version: <version>.<sub_version1>.<sub_version2> 
     00000000           00000                                                                                           
        000000         000                                                                                              
          0000000    000          


 
    '''
    return logo.replace('<version>', v).replace('<sub_version1>', sv).replace('<sub_version2>', str(sv2))



if __name__ == '__main__':
    print cafe_logo('v1','19')