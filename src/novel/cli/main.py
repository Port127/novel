import click
import sys
from novel.pipeline.project_manager import ProjectManager

@click.group()
def cli():
    """Novel V2 CLI: A Multi-Agent Novel Generation Engine."""
    pass

@cli.command()
@click.argument("name")
@click.option("--genre", default="修仙", help="Genre of the novel.")
@click.option("--author", default="匿名", help="Author name.")
@click.option("--template", default="default", help="Template to use.")
def new(name: str, genre: str, author: str, template: str):
    """Create a new novel project."""
    pm = ProjectManager()
    try:
        project_id = pm.create_project(name=name, genre=genre, author=author, template=template)
        click.secho(f"✅ Project created successfully: {project_id}", fg="green")
        click.echo(f"   Name: {name}")
        click.echo(f"   Genre: {genre}")
    except ValueError as e:
        click.secho(f"❌ Error: {str(e)}", fg="red")
        sys.exit(1)

@cli.command()
def list():
    """List all novel projects."""
    pm = ProjectManager()
    projects = pm.list_projects()
    
    if not projects:
        click.echo("No projects found.")
        return
        
    click.echo(f"Found {len(projects)} projects:")
    click.echo("-" * 60)
    for p in projects:
        click.echo(f"  {p['id']}")
        click.echo(f"    Name: {p['name']} | Genre: {p['genre']} | Status: {p['status']}")
    click.echo("-" * 60)

@cli.command()
@click.argument("project_id")
def delete(project_id: str):
    """Delete a novel project by ID."""
    pm = ProjectManager()
    if pm.delete_project(project_id):
        click.secho(f"✅ Project {project_id} deleted.", fg="green")
    else:
        click.secho(f"❌ Project {project_id} not found.", fg="red")
        sys.exit(1)

@cli.command()
@click.argument("project_id")
def show(project_id: str):
    """Show details of a novel project."""
    pm = ProjectManager()
    data = pm.show_project(project_id)
    if not data:
        click.secho(f"❌ Project {project_id} not found.", fg="red")
        sys.exit(1)
        
    click.echo(f"Project Details: {project_id}")
    click.echo("=" * 60)
    click.echo(f"Name: {data.get('name')}")
    click.echo(f"Author: {data.get('author')}")
    click.echo(f"Genre: {data.get('genre')}")
    click.echo("=" * 60)

if __name__ == "__main__":
    cli()
