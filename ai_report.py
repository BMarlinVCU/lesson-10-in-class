from groq import Groq 
import os

def make_report(weather_data):
    client=Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )

    response=client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role":"system",
                "content":("you are a weather reporter"
                           "write a short but witty report about"
                           "the provided weather data"
                           "do not make weather stuff up.")
            },
            {"role":"user",
            "content":weather_data.to_string(index=False)}
            # "content":weather_data}
        ],
        reasoning_effort="low"
    )

    report=response.choices[0].message.content
    usage=response.usage
    return report,usage

def ask_question(weather_data, messages):
    client=Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )

    response=client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role":"system",
             "content":"Answer using only this weather data. If it is not in the data, say so.\n"
                       +weather_data.to_string(index=False)}
        ]+messages,
        reasoning_effort="low"
    )

    return response.choices[0].message.content

if __name__=="__main__":
    print(make_report("25 degrees and snow."))