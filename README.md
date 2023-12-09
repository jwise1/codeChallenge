# codeChallenge

Program to analyze SMART goal formation. User tells program what their goals are, and program helps user understand the specifics of the goal using the SMART method(Specific, measurable, achievable, relevant, time-based).
Uses Google T5-large pretrained model as well as transformers library, pytorch, and accelerate packages. 

First version: interact with chat application to fine tune goals using SMART method. Didn't take previous answers from users into account but built on overall goal. 

Second version: interact with chat application to fine tune goals using SMART attributes. Took previous user answers into account as well as overall goal. 


