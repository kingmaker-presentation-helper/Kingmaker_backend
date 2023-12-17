import ast
import os

async def process_data(session_key, tag):
    try:
        if tag == "statement":
            # open asr.txt and read the content
            with open(f'user/{session_key}/asr.txt', 'r', encoding="utf-8") as f:
                # 1번째 줄을 읽어서 저장
                for i in range(1):
                    statement = f.readline()
            return statement
        
        elif tag == "keyword":
            # open generated_keyword.txt and read the content(dictionary)
            with open(f'user/{session_key}/generated_keyword.txt', 'r', encoding="utf-8") as f:
                keyword = f.read()
            # convert string to dictionary
            keyword = ast.literal_eval(keyword)

            return keyword
        
        elif tag == "question":
            # open generated_question.txt and read the content(dictionary)
            with open(f'user/{session_key}/generated_question.txt', 'r', encoding="utf-8") as f:
                question = f.read()
            # convert string to dictionary
            question = ast.literal_eval(question)

            return question

        elif tag == "duration":
            # open duration.txt and read the content
            with open(f'user/{session_key}/duration.txt', 'r', encoding="utf-8") as f:
                duration = f.read()

            return duration
        
        elif tag == "count_of_pose":
            # open capture folder and count the number of images
            path = f'user/{session_key}/capture'
            files = os.listdir(path)
            images = len(files)

            return images
        
        elif tag == "pose":
            # open capture folder and return images
            path = f'user/{session_key}/capture'
            files = os.listdir(path)
            images = []
            for file in files:
                images.append(file)
            
            return images
                
        elif tag == "highlight":
            # open highlight.txt and read the content(dictionary)
            with open(f'user/{session_key}/highlight.txt', 'r', encoding="utf-8") as f:
                highlight = f.read()
            # convert string to dictionary
            highlight = ast.literal_eval(highlight)

            return highlight
        
        elif tag == "pronunciation":
            # open pronunciation.txt and read the content
            with open(f'user/{session_key}/asr.txt', 'r', encoding="utf-8") as f:
                # 2번째 줄을 읽어서 저장
                for i in range(2):
                    pronunciation = f.readline()

            return pronunciation
        
        else:
            raise ValueError(f"Invalid tag: {tag}")
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
        # Handle the FileNotFoundError, log, or re-raise the exception if needed
    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle other exceptions, log, or re-raise the exception if needed
