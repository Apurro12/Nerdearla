import base64 
from openai import OpenAI 
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("images")

client = OpenAI() 

@mcp.tool()
def extract_data_from_image(image_path: str) -> str:
    """
    Extract information from a base64 encoded image using OCR.

    Args:
        image_path: Path to the image file.
    Returns:
        Extracted data from the image.
    """
    # Function to encode the image
    #image_path = "/Users/camiloleonel/Desktop/cintia.png"
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    # Getting the Base64 string
    base64_image = encode_image(image_path)

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "How much money I've transfered"
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            } # type: ignore
        ],
    )
    return response.output_text


mcp.run(transport="streamable-http")