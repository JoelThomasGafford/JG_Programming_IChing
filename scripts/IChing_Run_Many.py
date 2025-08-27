from IChing_Class import IChingCaster
from pathlib import Path
from datetime import datetime




caster = IChingCaster()

log_path = Path(__file__).with_name("IChing_log_main.txt")

question = ""
while True:
    now = datetime.now().isoformat(sep=' ', timespec='milliseconds')
    question = input(f"What is your question as of {now}?: ")
    # if question.lower() == "bye":
    #     print("Goodbye")
    #     break

    resp = caster.cast_text()
    print(resp)
    print()
    print("=" * 100)
    print()

    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"Question as of {now} is: {question}")
        log.write("\n\n")
        log.write(resp)
        log.write("\n\n")
        log.write("=" * 100)
        log.write("\n\n")