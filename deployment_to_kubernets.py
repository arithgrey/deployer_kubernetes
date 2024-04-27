import os
import re
from dotenv import dotenv_values

def load_env_vars(env_file=".env"):
    try:
        return dotenv_values(env_file)
    except Exception as e:
        print(f"Error loading environment variables from {env_file}: {e}")
        exit(1)

def load_template(template_file):
    try:
        with open(template_file, "r") as template:
            return template.read()
    except Exception as e:
        print(f"Error loading template file {template_file}: {e}")
        exit(1)

def find_and_replace_variables(content, env_vars):
    pattern = r"\{(\w+)\}"
    replaced_content = re.sub(pattern, lambda x: env_vars.get(x.group(1), x.group(0)), content)
    return replaced_content

def generate_deployment(input_dir="ci/next", output_dir="ci/k8s", output_file="deploy.yaml"):
    env_vars = load_env_vars()
    output_content = ""

    try:
        # Crea el directorio de salida si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Crea el directorio de plantillas si no existe
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)

        # Itera sobre los archivos en el directorio de entrada
        for filename in os.listdir(input_dir):
            input_file = os.path.join(input_dir, filename)
            if os.path.isfile(input_file):
                template_content = load_template(input_file)
                replaced_content = find_and_replace_variables(template_content, env_vars)
                output_content += replaced_content.strip() + "\n---\n"
        
        # Escribe el contenido en el archivo de salida
        output_path = os.path.join(output_dir, output_file)
        with open(output_path, "w") as output:
            output.write(output_content.strip("\n---\n"))
        
        print(f"Deployment file '{output_file}' generated successfully in '{output_dir}' directory.")
    except Exception as e:
        print(f"Error generating deployment file: {e}")
        exit(1)

if __name__ == "__main__":
    generate_deployment()
