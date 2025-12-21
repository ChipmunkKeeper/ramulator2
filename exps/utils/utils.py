

def save_ramulator_output(stdout: str, result_filename: str,) -> None:
    """
    save output as YAML file, commenting out lines that start with '['.
    stdout: Ramulator输出内容
    result_filename: 结果保存路径
    """
    with open(result_filename, 'w') as result_file:
        for line in stdout.splitlines():
            # 如果行以 '[' 开头（Ramulator 的日志特征），则加上 '#' 变成 YAML 注释
            if line.strip().startswith('['):
                result_file.write(f"# {line}\n")
            else:
                # YAML 内容
                result_file.write(f"{line}\n")
    print(f"Results saved to: {result_filename}")