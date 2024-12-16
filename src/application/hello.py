import asyncio

async def async_function(duration):
    print(f"録音を開始します。録音時間: {duration}秒")
    await asyncio.sleep(duration)
    print("録音が終了しました。")

def hello_world():
    print("Hello, world!")
    return "Hello, world!"

if __name__ == "__main__":
    hello_world()