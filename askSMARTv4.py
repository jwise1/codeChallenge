from transformers import pipeline, AutoTokenizer
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

def formQuestion(message):
    attr=["specific","measurable","achievable","relevant","time-based"]
    for i in attr:
        prompt=f"""Write a question about completing the following goal: "{message}", in a "{i}" way."""
        q=pipe(prompt,max_new_tokens=25,eos_token_id=tokenizer.eos_token_id)
        newMessage=talkToUser(q)
        followUp(newMessage,message,i)

def followUp(newMessage,message,i):
    prompt=f"""Does this answer: "{newMessage}" address completing this goal: "{message}", in a "{i}" way? Yes or no."""
    q=pipe(prompt,max_new_tokens=25,eos_token_id=tokenizer.eos_token_id)
    if q[0]['generated_text']=="No":
        prompt=f"""Write a question about completing this goal: "{message}", in a MORE "{i}" way."""
        q=pipe(prompt,max_new_tokens=25,eos_token_id=tokenizer.eos_token_id)
        newMessage=talkToUser(q)
        #followUp(newMessage,message,i)

def main():
    initQ="What is one of your current goals?"
    message=talkToUser(initQ)
    formQuestion(message)
    
if __name__ == "__main__":
    main()