import random
import string


# --- 问题1: 随机字符串正序子串查询 ---

def find_longest_ascending_substring(s):
    """
    查找字符串中单个最长的相邻字符正序子串。
    "正序" 指的是严格递增，例如 "ac" (ord('c') > ord('a'))。 "aa" 不是。
    """
    if not s:
        return ""

    max_substring = ""
    current_substring = ""

    for char in s:
        if not current_substring or ord(char) > ord(current_substring[-1]):
            current_substring += char
        else:
            # 当前字符不大于前一个字符，正序中断
            if len(current_substring) > len(max_substring):
                max_substring = current_substring
            # 开始新的子串，以当前字符开头 (如果当前字符和前一个相同，则新子串从当前字符开始)
            # 如果当前字符小于前一个，也从当前字符开始
            current_substring = char
            # 修正：如果 aa, current_substring 会是 "a", 然后又 "a"
            # 如果是"cba", current_substring 会是 "c", max_substring="c"
            # 然后 current_substring="b", max_substring="c"
            # 然后 current_substring="a", max_substring="c"
            # 这一逻辑在之前是：
            # # 开始新的子串，以当前字符开头
            # current_substring = char
            # 但如果遇到 "aa", 它应该中断。
            # "aa" 不是正序。 "ab" 是。
            # if "aa", char='a', current_substring[-1]='a'. ord(char) > ord(current_substring[-1]) is False.
            # So, it goes to else. max_substring (if "a" was previous) is "a".
            # current_substring becomes "a". This is correct. "aa" won't form "aa".

    # 循环结束后，最后检查一次 current_substring
    if len(current_substring) > len(max_substring):
        max_substring = current_substring

    # 如果最长子串只有一个字符，且原字符串不为空，这是有效的。
    # (例如 "zyxwv", 最长的是 "z" (或 "y" or "x"...), 我的代码会返回 "z")
    # 题目说 "ac" is正序, "aa" is not. This implies a length of at least 2 for "正序子串".
    # 但如果找不到长度>=2的，最长的就是单个字符。
    # 如果题目严格要求正序子串长度必须 >= 2，则需要在这里加判断
    # if len(max_substring) < 2: return ""
    # 但通常这种问题，单个字符也被视为长度为1的子串。
    # 鉴于 "aa" 不是，那么单个字符 "a" 本身也不是 "正序子串" 的典型例子，
    # 但它是一个子串，并且是 "最长的" (如果没有更长的)。
    # 为了清晰，如果找不到长度大于1的正序子串，返回空字符串或第一个字符。
    # 样例输出是 "abcdefg"，长度远大于1。
    # Let's assume a single character is a valid (though trivial) "longest" if no longer sequence exists.
    # The current logic correctly handles finding sequences like "abc". If only "cba" exists, it finds "c".

    return max_substring


def generate_random_string(length, alphabet=string.ascii_lowercase):
    """生成指定长度的随机字符串"""
    return ''.join(random.choice(alphabet) for _ in range(length))


def main_problem1():
    print("--- 问题1: 随机字符串正序子串查询 ---")
    num_strings = 100  # 题目要求100个
    # 字符集从 'a' 到 'z'，因为样例输出有 'g'，超出了 'a'-'f' 的范围
    # 题目原文 "abcdef" 字符串，可能指字符来源是 a-f，也可能指这是一个例子。
    # 我选择 a-z 因为样例输出是 "abcdefg"
    alphabet = string.ascii_lowercase

    overall_longest_substring_global = ""

    print("\n部分随机字符串及其最长正序子串示例：")
    for i in range(num_strings):
        # 随机长度，例如 20 到 50
        str_len = random.randint(20, 50)
        random_str = generate_random_string(str_len, alphabet)

        longest_in_current_str = find_longest_ascending_substring(random_str)

        if len(longest_in_current_str) > len(overall_longest_substring_global):
            overall_longest_substring_global = longest_in_current_str
        elif len(longest_in_current_str) == len(overall_longest_substring_global) and \
                longest_in_current_str < overall_longest_substring_global:
            # 如果长度相同，选择字典序较小的（可选，题目未明确）
            overall_longest_substring_global = longest_in_current_str

        if i < 3:  # 只打印前3个作为示例
            print(f"随机字符串 ({i + 1}): {random_str}")
            print(f"最长正序子串: {longest_in_current_str if longest_in_current_str else '无 (或仅单字符)'}\n")

    print(
        f"\n在{num_strings}个随机字符串中，找到的全局最长正序子串是: '{overall_longest_substring_global}' (长度: {len(overall_longest_substring_global)})")

    print("\n题目样例验证:")
    # 题目提供的随机字符串样例
    sample_str_from_problem = "aefebfedfacbabceeffdabcdeffacdeffdabdeffafacbbfedf"
    # 题目提供的最长正序子串样例输出 (它不源于上面的随机字符串)
    sample_output_from_problem = "abcdefg"

    print(f"题目提供的随机字符串: {sample_str_from_problem}")
    result_for_sample_input = find_longest_ascending_substring(sample_str_from_problem)
    print(f"对其运行查找函数的结果: '{result_for_sample_input}' (长度: {len(result_for_sample_input)})")
    # For "aefebfedfacbabceeffdabcdeffacdeffdabdeffafacbbfedf", my code finds "aef" or "abc" or "deff" etc.
    # The longest are "deff", "abce", "acde". The first one encountered of max length.
    # aef (3)
    # abc (3)
    # abcd (4) -> No, 'd' is not > 'c' in 'abcdeff', it's 'c' 'd' 'e'.
    # For "dabcdeff", it is "abcde" (5)
    # Let's re-trace "aefebfedfacbabceeffdabcdeffacdeffdabdeffafacbbfedf"
    # aef (len 3)
    # eb -> e
    # fe -> f
    # ed -> e
    # df -> d
    # fa -> f
    # ac (len 2)
    # cb -> c
    # ba -> b
    # abc (len 3)
    # ee -> e
    # ef (len 2)
    # ff -> f
    # fd -> f
    # abcd (len 4) -> in "dabcdeff"
    # eff (len 3) -> in "deff"
    # acd (len 3) -> in "acdeff"
    # eff (len 3) -> in "deff"
    # abd (len 3) -> in "dabdeff"
    # eff (len 3) -> in "deff"
    # af (len 2)
    # ac (len 2)
    # bb -> b
    # bf (len 2)
    # fe -> f
    # ed -> e
    # df -> d
    # The actual longest for "aefebfedfacbabceeffdabcdeffacdeffdabdeffafacbbfedf" is "abcde" (from "dabcdeff").
    # Let's test with `find_longest_ascending_substring("dabcdeff")` -> `abcde`
    # The string `sample_str_from_problem` contains `abcde` within `dabcdeff`.

    print(f"题目提供的最长正序子串样例输出: '{sample_output_from_problem}'")
    print(f"  这个样例输出 '{sample_output_from_problem}' 并不来自上面提供的随机字符串。")
    print(f"  如果一个字符串包含 '{sample_output_from_problem}', 函数会找到它:")
    test_str_containing_sample_output = "xy" + sample_output_from_problem + "mn"
    print(
        f"  测试 '{test_str_containing_sample_output}': '{find_longest_ascending_substring(test_str_containing_sample_output)}'")


# --- 问题2: 函数设计 sum15() ---

def sum15(numbers):
    """
    计算列表的和，但如果列表中存在15，则15和15之后的一个数字均不进行求和。
    """
    total_sum = 0
    i = 0
    n = len(numbers)

    while i < n:
        if numbers[i] == 15:
            i += 2  # 跳过15和它后面的一个数字 (索引增加2)
        else:
            total_sum += numbers[i]
            i += 1  # 索引增加1

    return total_sum


def main_problem2():
    print("\n--- 问题2: 函数设计 sum15() ---")

    # 第一个样例
    list1_str = "[1, 2, 15, 9, 5]"  # 题目未给出输入，仅有 sum15()的返回值为 6
    # 假设输入是这个，以便得到6。
    # 1+2 = 3. 遇到15, 跳过15和9. 下一个5. 3+5=8.
    # 为了得到6，如果列表是 [1,2,3,15,any,any,...] 1+2+3 = 6. 15及之后不加。
    # 或者 [6, 15, any, any, ...]
    # 题目给的样例是： sum15([1,2,15,9,5])的返回值为 6.
    # 这与规则 “15和15之后的一个数字均不进行求和” 有冲突。
    # 按照规则：[1,2,15,9,5] -> 1+2 (15,9跳过) + 5 = 8.

    # 我将按规则实现，并指出样例的差异
    list1_from_example = [1, 2, 15, 9, 5]
    expected_output1_from_example = 6
    actual_output1 = sum15(list1_from_example)
    print(f"sum15({list1_from_example})")
    print(f"  题目预期输出: {expected_output1_from_example}")
    print(f"  函数按规则实际输出: {actual_output1}")
    if actual_output1 != expected_output1_from_example:
        print(f"  注意：实际输出 ({actual_output1}) 与题目预期 ({expected_output1_from_example}) 不符。")
        print(f"  根据规则“15和15之后的一个数字均不进行求和”：")
        print(f"    对于列表 {list1_from_example}: 1 + 2 = 3. 遇到15，跳过15和其后的9. 下一个数字是5. 总和 = 3 + 5 = 8.")
        print(f"    若要得到6，可能的输入是例如 [1,2,3,15,...] (1+2+3=6，15及其后一个被跳过)。")

    # 第二个样例
    list2_str = "[10,1,2,15,9,1,10]"  # 题目未给出输入，仅有 sum15()的返回值为 24
    # 假设输入是这个，以便得到24。
    # 10+1+2 = 13. 遇到15, 跳过15和9. 下一个1. 13+1=14. 下一个10. 14+10=24. 这个吻合规则。
    list2_from_example_assumption = [10, 1, 2, 15, 9, 1, 10]
    expected_output2_from_example = 24
    actual_output2 = sum15(list2_from_example_assumption)
    print(f"\nsum15({list2_from_example_assumption}) (假设这是第二个样例的输入)")
    print(f"  题目预期输出: {expected_output2_from_example}")
    print(f"  函数按规则实际输出: {actual_output2}")
    if actual_output2 == expected_output2_from_example:
        print(f"  实际输出与题目预期相符。")

    print(f"\n更多测试用例:")
    print(f"sum15([1, 2, 3, 4, 5])       -> {sum15([1, 2, 3, 4, 5])} (预期 15)")
    print(f"sum15([15, 1, 2, 3])         -> {sum15([15, 1, 2, 3])} (预期 2+3=5)")
    print(f"sum15([1, 15, 2, 3])         -> {sum15([1, 15, 2, 3])} (预期 1+3=4)")
    print(f"sum15([1, 2, 15])            -> {sum15([1, 2, 15])} (预期 1+2=3, 15被跳过，后面没数字)")
    print(f"sum15([15])                  -> {sum15([15])} (预期 0)")
    print(f"sum15([])                    -> {sum15([])} (预期 0)")
    print(f"sum15([15, 5, 15, 3, 8])     -> {sum15([15, 5, 15, 3, 8])} (预期 8)")  # 跳过15,5; 跳过15,3; 加8.


# --- 问题3: 随机验证码生成程序 ---

def generate_captcha():
    """
    生成一个符合要求的9位随机验证码。
    要求：包含大小写字母、数字、指定特殊字符。
    """
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_chars = "!@#$%^&*"  # 题目指定8个

    # 1. 确保每种类型的字符至少有一个
    guaranteed_chars = []
    guaranteed_chars.append(random.choice(uppercase_letters))
    guaranteed_chars.append(random.choice(lowercase_letters))
    guaranteed_chars.append(random.choice(digits))
    guaranteed_chars.append(random.choice(special_chars))

    # 2. 剩余的字符 (9 - 4 = 5) 从所有可用字符中随机选择
    all_possible_chars = uppercase_letters + lowercase_letters + digits + special_chars
    remaining_length = 9 - len(guaranteed_chars)

    for _ in range(remaining_length):
        guaranteed_chars.append(random.choice(all_possible_chars))

    # 3. 打乱字符顺序，使得固定添加的字符位置随机
    random.shuffle(guaranteed_chars)

    return "".join(guaranteed_chars)


def main_problem3():
    print("\n--- 问题3: 随机验证码生成程序 ---")
    print("程序将持续生成9位验证码。")
    print("验证码要求：长度为9，由英文字母（必须有大小写），数字，及特殊字符(!@#$%^&*)组成。")
    print("直接按 Enter 键退出程序。\n")

    while True:
        captcha = generate_captcha()
        print(f"生成的验证码: {captcha}")

        # 验证一下生成的验证码是否符合要求（可选步骤，用于开发时调试）
        # has_upper = any(c.isupper() for c in captcha)
        # has_lower = any(c.islower() for c in captcha)
        # has_digit = any(c.isdigit() for c in captcha)
        # has_special = any(c in "!@#$%^&*" for c in captcha)
        # if not (has_upper and has_lower and has_digit and has_special and len(captcha)==9):
        #     print(f"警告: 生成的验证码 '{captcha}' 不完全符合要求!")

        user_input = input("按 Enter 键退出，按其他任意键并回车可生成下一个验证码: ")
        if not user_input:  # 用户直接按了回车 (空字符串)
            print("程序退出。")
            break
        # else: continue to next iteration


# --- 主程序入口 ---
if __name__ == "__main__":
    # --- 问题1 ---
    main_problem1()
    print("\n" + "=" * 70 + "\n")  # 分隔线

    # --- 问题2 ---
    main_problem2()
    print("\n" + "=" * 70 + "\n")  # 分隔线

    # --- 问题3 ---
    main_problem3()
