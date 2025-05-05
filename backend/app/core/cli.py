import asyncio
from typing import Optional

import typer
from rich import print
from rich.console import Console
from rich.prompt import Confirm, Prompt
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.security import get_password_hash
from app.crud.crud_user import user as crud_user
from app.schemas.user import UserCreate

app = typer.Typer(help="CLI do Licitação Hub", add_completion=False)
console = Console()


async def get_db_session():
    """
    # Cria uma sessão de banco de dados para uso nos comandos CLI
    # Create a database session for CLI commands use
    """
    engine = create_async_engine(str(settings.DATABASE_URL))
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.commit()


@app.command()
def run_migrations():
    """
    # Executa migrações do banco de dados
    # Run database migrations
    """
    import subprocess
    
    console.print("[bold green]Executando migrações do banco de dados...[/bold green]")
    result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
    
    if result.returncode == 0:
        console.print("[bold green]✓[/bold green] Migrações concluídas com sucesso!")
        if result.stdout:
            console.print(result.stdout)
    else:
        console.print("[bold red]✗ Erro ao executar migrações:[/bold red]")
        console.print(result.stderr)


@app.command()
def create_superuser():
    """
    # Cria um usuário administrador
    # Create an admin user
    """
    async def _create_superuser():
        try:
            # Solicitar dados do usuário
            # Request user data
            console.print("[bold blue]Criação de Usuário Administrador[/bold blue]")
            console.print("Por favor, forneça as informações solicitadas:")
            
            email = Prompt.ask("Email", default=settings.FIRST_SUPERUSER_EMAIL)
            username = Prompt.ask("Nome de usuário", default=email.split("@")[0])
            first_name = Prompt.ask("Nome")
            last_name = Prompt.ask("Sobrenome")
            password = Prompt.ask("Senha", password=True, default=settings.FIRST_SUPERUSER_PASSWORD)
            
            # Confirmar os dados
            # Confirm data
            console.print("\n[bold]Verifique os dados:[/bold]")
            console.print(f"Email: {email}")
            console.print(f"Nome de usuário: {username}")
            console.print(f"Nome: {first_name} {last_name}")
            
            if not Confirm.ask("\nConfirma a criação do usuário?"):
                console.print("[yellow]Operação cancelada pelo usuário.[/yellow]")
                return
            
            # Criar o usuário
            # Create user
            user_data = UserCreate(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Obter uma sessão de banco de dados
            # Get a database session
            db_gen = get_db_session()
            db = await anext(db_gen)
            
            # Verificar se já existe um usuário com este email
            # Check if a user with this email already exists
            existing_user = await crud_user.get_by_email(db, email=email)
            if existing_user:
                console.print(f"[bold red]✗ Já existe um usuário com o email {email}[/bold red]")
                return
            
            # Verificar se já existe um usuário com este nome de usuário
            # Check if a user with this username already exists
            existing_user = await crud_user.get_by_username(db, username=username)
            if existing_user:
                console.print(f"[bold red]✗ Já existe um usuário com o nome de usuário {username}[/bold red]")
                return
            
            # Criar o usuário e definir como administrador
            # Create user and set as admin
            user = await crud_user.create(db, obj_in=user_data)
            user.is_admin = True
            await db.commit()
            
            console.print("[bold green]✓ Usuário administrador criado com sucesso![/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]✗ Erro ao criar usuário: {str(e)}[/bold red]")
    
    asyncio.run(_create_superuser())


@app.command()
def init_db():
    """
    # Inicializa o banco de dados com dados iniciais
    # Initialize the database with initial data
    """
    if Confirm.ask("Isso irá criar tabelas e dados iniciais. Continuar?"):
        run_migrations()
        console.print("[bold green]✓[/bold green] Banco de dados inicializado!")
        
        if Confirm.ask("Deseja criar um usuário administrador?"):
            create_superuser()


if __name__ == "__main__":
    app()
