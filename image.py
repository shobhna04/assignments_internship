                                                                                                                                        import requests

                                                                                                                                        user_prompt = "joey tribiani from friends,more realistic wearing a kincks t shirt and siiting with the hugsy"
                                                                                                                                        url = f"https://image.pollinations.ai/prompt/{user_prompt.replace(' ', '%20')}"

                                                                                                                                        print(f"generating for: {user_prompt}")

                                                                                                                                        response = requests.get(url)

                                                                                                                                        if response.status_code == 200:
                                                                                                                                            with open("GOAT.png", "wb") as file:
                                                                                                                                                file.write(response.content)
                                                                                                                                            print("success")
                                                                                                                                        else:
                                                                                                                                            print("error")