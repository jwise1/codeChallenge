from transformers import pipeline, AutoTokenizer,AutoModel
import torch

model = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model)
pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
)
def talkToUser(message):
    try:
        message=message[0]['generated_text']
    except Exception:
        print("Formatting skipped, welcome to SMART goal analyzer program.")
    userIn=input(message+"\n")
    return userIn

def formQuestion(message,newMessage,i):
    initQ="What is one of your current goals?"
    if i==0:
        message=talkToUser(initQ)
        newMessage=message
    else:
        if i==1:
            prompt="""Write a question about breaking down the steps to the following goal more specifically: """+message
            q=pipe(prompt,max_new_tokens=25,eos_token_id=tokenizer.eos_token_id)
            newMessage=talkToUser(q)
        if i==2:
            prompt="""Write a question about how to measure the goal: """+message+""" while also considering the previous answer to how to meet the goal: """+newMessage
            q=pipe(prompt,max_new_tokens=25,eos_token_id=tokenizer.eos_token_id)
            newMessage=talkToUser(q)
        if i==3:
            prompt="""Write a question about how achievable the goal is: """+message+""" while also considering the previous answer to how to meet the goal: """+newMessage
            q=pipe(prompt,max_new_tokens=25,eos_token_id=tokenizer.eos_token_id)
            newMessage=talkToUser(q)
        if i==4:
            prompt="""Write a question about how relevant the goal is overall: """+message+""" while also considering the previous answer to how to meet the goal: """+newMessage
            q=pipe(prompt,max_new_tokens=25,eos_token_id=tokenizer.eos_token_id)
            newMessage=talkToUser(q)
        if i==5:
            prompt="""Write a question about the how much time it will take to complete the goal: """+message+""" while also considering the previous answer to how to meet the goal: """+newMessage
            q=pipe(prompt,max_new_tokens=25,eos_token_id=tokenizer.eos_token_id)
            newMessage=talkToUser(q)

        followUp(newMessage,message,i)
    return message,newMessage

def followUp(newMessage,message,i):
    if i==1:
        prompt="""Does this answer: """+newMessage+""" address this goal: """+message+""" more specifically? Yes or no."""
        q=pipe(prompt,max_new_tokens=25)
        if q[0]['generated_text']=="No":
            prompt="""Write a question to ask more specifically how this goal can be broken down into smaller steps: """+message
            q=pipe(prompt,max_new_tokens=25)
            newMessage=talkToUser(q)
            #followUp(newMessage,message,i)
    if i==2:
        prompt="""Does this answer: """+newMessage+""" address this goal: """+message+""" in a measured way? Yes or no."""
        q=pipe(prompt,max_new_tokens=25)
        if q[0]['generated_text']=="No":
            prompt="""Write a question to ask how to better measure this goal quantifiably: """+message
            q=pipe(prompt,max_new_tokens=25)
            newMessage=talkToUser(q)
            #followUp(newMessage,message,i)
    if i==3:
        prompt="""Does this answer: """+newMessage+""" address this goal: """+message+""" with how it can be achieved? Yes or no."""
        q=pipe(prompt,max_new_tokens=25)
        if q[0]['generated_text']=="No":
            prompt="""Write a question to ask how this goal can be achieved through actions: """+message
            q=pipe(prompt,max_new_tokens=25)
            newMessage=talkToUser(q)
            #followUp(newMessage,message,i)
    if i==4:
        prompt="""Does this answer: """+newMessage+""" address this goal: """+message+""" relevantly to a human? Yes or no."""
        q=pipe(prompt,max_new_tokens=25)
        if q[0]['generated_text']=="No":
            prompt="""Write a question to ask how this goal can be relevantly addressed in one's life: """+message
            q=pipe(prompt,max_new_tokens=25)
            newMessage=talkToUser(q)
            #followUp(newMessage,message,i)
    if i==5:
        prompt="""Does this answer: """+newMessage+""" address this goal: """+message+""" with time considerations? Yes or no."""
        q=pipe(prompt,max_new_tokens=25)
        if q[0]['generated_text']=="No":
            prompt="""Write a question to ask how this goal can be more timely thought of in terms of weeks, months and years: """+message
            q=pipe(prompt,max_new_tokens=25)
            newMessage=talkToUser(q)
            #followUp(newMessage,message,i)

def main():
    resp=""
    message=""
    for i in range(0,5):
        message, resp=formQuestion(message,resp,i)
    
if __name__ == "__main__":
    main()
