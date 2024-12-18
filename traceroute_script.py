import argparse
import subprocess
import re
import platform

def traceroute(url_or_ip, progressive=False, output_file=None):
    # Détection de l'OS
    is_windows = platform.system().lower() == "windows"
    command = ["tracert", url_or_ip] if is_windows else ["traceroute", url_or_ip]
    result_lines = []

    try:
        if progressive:
            # Mode progressif : Affichage au fur et à mesure avec subprocess.Popen
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            file = open(output_file, "w") if output_file else None  # Ouvre le fichier si spécifié
            try:
                for line in process.stdout:
                    ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                    if ip_match:
                        ip = ip_match.group(1)
                        print(ip)  # Affichage progressif
                        result_lines.append(ip)
                        if file:  # Écriture progressive dans le fichier
                            file.write(ip + "\n")
            finally:
                if file:  # Ferme le fichier si ouvert
                    file.close()
        else:
            # Mode par défaut : Affichage après exécution complète avec subprocess.run
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in result.stdout.splitlines():
                ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                if ip_match:
                    ip = ip_match.group(1)
                    result_lines.append(ip)

            # Affichage des résultats après exécution complète
            for ip in result_lines:
                print(ip)

            # Enregistrement des résultats dans un fichier si spécifié
            if output_file:
                with open(output_file, "w") as file:
                    file.write("\n".join(result_lines) + "\n")

    except FileNotFoundError:
        print(f"Erreur : La commande '{'tracert' if is_windows else 'traceroute'}' n'est pas disponible sur ce système.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traceroute Script TP6")
    parser.add_argument("url_or_ip", help="URL ou adresse IP à tracer")
    parser.add_argument("-p", "--progressive", action="store_true", help="Affiche les IPs des sauts au fur et à mesure")
    parser.add_argument("-o", "--output-file", help="Nom du fichier pour enregistrer les résultats")
    args = parser.parse_args()

    traceroute(args.url_or_ip, args.progressive, args.output_file)

