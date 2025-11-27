import time

from sqlalchemy import text


def wait_for_db(db, app, max_retries=30, retry_interval=1):
    """
    Aguarda o banco de dados estar disponível antes de prosseguir.

    Args:
        db: Instância do SQLAlchemy
        app: Instância do Flask app
        max_retries: Número máximo de tentativas (padrão: 30)
        retry_interval: Intervalo em segundos entre tentativas (padrão: 1)

    Returns:
        bool: True se conectou com sucesso, False caso contrário

    Raises:
        Exception: Se não conseguir conectar após max_retries tentativas
    """
    retries = 0
    while retries < max_retries:
        try:
            with app.app_context():
                # Tenta executar uma query simples para verificar a conexão
                db.session.execute(text("SELECT 1"))
                db.session.commit()
                print("✓ Banco de dados conectado com sucesso!")
                return True
        except Exception as e:
            retries += 1
            if retries < max_retries:
                print(
                    f"⏳ Aguardando banco de dados... (tentativa {retries}/{max_retries})"
                )
                time.sleep(retry_interval)
            else:
                print(
                    f"✗ Falha ao conectar ao banco de dados após {max_retries} tentativas: {e}"
                )
                raise
    return False
