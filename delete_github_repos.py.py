import github
import getpass
import sys

def delete_all_repos(token):
    """
    Удаляет все репозитории на GitHub аккаунте, связанном с предоставленным токеном.
    """
    try:
        g = github.Github(token)
        user = g.get_user()
        username = user.login
        print(f"Авторизован как: {username}")


        repos = user.get_repos()
        num_repos = repos.totalCount
        print(f"Найдено репозиториев: {num_repos}")

        if num_repos == 0:
            print("Нет репозиториев для удаления.")
            return

        print("ВНИМАНИЕ:  Все репозитории будут удалены БЕЗВОЗВРАТНО.")
        confirmation = input(f"Вы уверены, что хотите удалить ВСЕ {num_repos} репозиториев пользователя {username}? (введите 'yes' для подтверждения): ")
        if confirmation.lower() != 'yes':
            print("Удаление отменено.")
            return


        for repo in repos:
            try:
                print(f"Удаляю репозиторий: {repo.name}...")
                repo.delete()
                print(f"Репозиторий {repo.name} удален.")
            except github.GithubException as e:
                print(f"Ошибка при удалении репозитория {repo.name}: {e}")
            except Exception as e:
                 print(f"Неожиданная ошибка при удалении {repo.name}: {e}")


        print("Все репозитории удалены.")

    except github.BadCredentialsException:
        print("Ошибка аутентификации.  Неверный токен.")
    except github.GithubException as e:
        print(f"Ошибка GitHub API: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


if __name__ == "__main__":
    #  Получение токена.  Предпочтительный способ (более безопасный).
    print("Для удаления репозиториев необходим Personal Access Token (PAT) с областью действия 'delete_repo'.")
    print("Создайте PAT здесь: https://github.com/settings/tokens (выберите 'delete_repo')")

    token = getpass.getpass("Введите ваш GitHub Personal Access Token (не отображается): ")

    if not token:
        print("Токен не введен.  Выполнение скрипта прервано.")
        sys.exit(1)
    
    delete_all_repos(token)