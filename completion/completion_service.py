import json
from sqlalchemy.orm import Session

from completion.completion_schemas import CompletionRequest
from completion.completion_utils import call_external_api

class CompletionService:
    @staticmethod
    def generate_completion(request: CompletionRequest, db: Session):
        messages = [msg.dict() for msg in request.messages]
        model = request.model
        params = {
            "max_tokens": request.maxTokens,
            "temperature": request.temperature,
            "top_p": request.topP,
            "top_k": request.topK,
            "repetition_penalty": request.repetitionPenalty,
            "min_p": request.minP,
        }

        response = call_external_api(messages, model, params)

        plain_text = ""
        def stream_response():
            nonlocal plain_text
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    # yield f"data: {decoded_line}\n\n"  # Ensure double newline(remove \n if not needed)
                    if decoded_line.startswith("data: "):
                        try:
                            json_line = json.loads(decoded_line[6:])
                            content = json_line.get("choices", [{}])[0].get("delta", {}).get("content")
                            if (content == None or not content):
                                yield 'DONE'
                                break
                            yield f"data: {content}\n\n"
                            #print(content)
                            if content:
                                plain_text += content
                        except Exception as e:
                            print(f"Failed to parse line: {decoded_line}, error: {e}")

            # temp_message = TempMessage(content=plain_text)
            # db.add(temp_message)
            # db.commit()

        return stream_response()
    
# class CompletionService:
#     @staticmethod
#     def generate_completion(request: CompletionRequest, db: Session):
#         # messages = request.messages
#         messages = [msg.dict() for msg in request.messages]
#         model = request.model
#         params = {
#             "max_tokens": request.maxTokens,
#             "temperature": request.temperature,
#             "top_p": request.topP,
#             "top_k": request.topK,
#             "repetition_penalty": request.repetitionPenalty,
#             "min_p": request.minP,
#         }

#         response = call_external_api(messages, model, params)
#         return response