parser grammar xDroneParser;

options {
  tokenVocab=xDroneLexer;
}

prog : func* MAIN L_PAR R_PAR L_BRACE commands R_BRACE ;

commands : command* ;

command
  : (expr DOT)? TAKEOFF L_PAR R_PAR SEMICOLON                                        #takeoff
  | (expr DOT)? LAND L_PAR R_PAR SEMICOLON                                           #land
  | (expr DOT)? UP L_PAR expr R_PAR SEMICOLON                                        #up
  | (expr DOT)? DOWN L_PAR expr R_PAR SEMICOLON                                      #down
  | (expr DOT)? LEFT L_PAR expr R_PAR SEMICOLON                                      #left
  | (expr DOT)? RIGHT L_PAR expr R_PAR SEMICOLON                                     #right
  | (expr DOT)? FORWARD L_PAR expr R_PAR SEMICOLON                                   #forward
  | (expr DOT)? BACKWARD L_PAR expr R_PAR SEMICOLON                                  #backward
  | (expr DOT)? ROTATE_LEFT L_PAR expr R_PAR SEMICOLON                               #rotateLeft
  | (expr DOT)? ROTATE_RIGHT L_PAR expr R_PAR SEMICOLON                              #rotateRight
  | (expr DOT)? WAIT L_PAR expr R_PAR SEMICOLON                                      #wait
  | type_ ident SEMICOLON                                                            #declare
  | type_ ident ARROW expr SEMICOLON                                                 #declareAssign
  | vectorElem ARROW expr SEMICOLON                                                  #assignVectorElem
  | listElem ARROW expr SEMICOLON                                                    #assignListElem
  | ident ARROW expr SEMICOLON                                                       #assignIdent
  | DEL ident SEMICOLON                                                              #del
  | expr (DOT AT L_PAR expr R_PAR)? DOT INSERT L_PAR expr R_PAR SEMICOLON            #insert
  | expr (DOT AT L_PAR expr R_PAR)? DOT REMOVE L_PAR R_PAR SEMICOLON                 #remove
  | call SEMICOLON                                                                   #procedureCall
  | IF expr L_BRACE commands R_BRACE (ELSE L_BRACE commands R_BRACE)?                #if
  | WHILE expr L_BRACE commands R_BRACE                                              #while
  | FOR ident FROM expr TO expr (STEP expr)? L_BRACE commands R_BRACE                #for
  | REPEAT expr TIMES L_BRACE commands R_BRACE                                       #repeat
  | RETURN (expr)? SEMICOLON                                                         #return
  | L_BRACE commands R_BRACE (PARALLEL L_BRACE commands R_BRACE)+ SEMICOLON          #parallel
  ;

ident : IDENT ;

listElem: expr L_BRACKET expr R_BRACKET ;

vectorElem
  : expr DOT VEC_X                                                          #vectorX
  | expr DOT VEC_Y                                                          #vectorY
  | expr DOT VEC_Z                                                          #vectorZ
  ;

funcIdent : IDENT ;

call : funcIdent L_PAR (argList)? R_PAR ;

argList: expr (COMMA expr)* ;

func
  : FUNCTION funcIdent L_PAR (paramList)? R_PAR RETURN type_ L_BRACE commands R_BRACE      #function
  | PROCEDURE funcIdent L_PAR (paramList)? R_PAR L_BRACE commands R_BRACE                  #procedure
  ;
paramList: type_ ident (COMMA type_ ident)* ;


type_
  : TYPE_INT                                   #intType
  | TYPE_DECIMAL                               #decimalType
  | TYPE_STRING                                #stringType
  | TYPE_BOOLEAN                               #booleanType
  | TYPE_VECTOR                                #vectorType
  | TYPE_DRONE                                 #droneType
  | TYPE_LIST L_BRACKET type_ R_BRACKET        #listType
  ;

expr
  : INT                                                     #intExpr
  | FLOAT                                                   #decimalExpr
  | ESCAPED_STRING                                          #stringExpr
  | TRUE                                                    #trueExpr
  | FALSE                                                   #falseExpr
  | ident                                                   #identExpr
  | expr L_BRACKET expr R_BRACKET                           #listElemExpr
  | expr DOT VEC_X                                          #vectorXExpr
  | expr DOT VEC_Y                                          #vectorYExpr
  | expr DOT VEC_Z                                          #vectorZExpr
  | L_BRACKET (expr (COMMA expr)*)? R_BRACKET               #list
  | L_PAR expr COMMA expr COMMA expr R_PAR                  #vector
  | call                                                    #functionCall
  | expr DOT SIZE                                           #size
  | L_PAR expr R_PAR                                        #parentheses
  | (PLUS | MINUS) expr                                     #positNegate
  | NOT expr                                                #not
  | expr (MULTI | DIV) expr                                 #multiDivide
  | expr (PLUS | MINUS) expr                                #plusMinus
  | expr CONCAT expr                                        #concat
  | expr (GREATER | GREATER_EQ | LESS | LESS_EQ) expr       #compare
  | expr (EQ | NOT_EQ) expr                                 #equality
  | expr AND expr                                           #and
  | expr OR expr                                            #or
  ;
