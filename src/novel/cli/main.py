import click
import sys
import asyncio
from novel.pipeline.project_manager import ProjectManager
from novel.pipeline.generation_pipeline import generate_worldbuilding, generate_characters, generate_outline
from novel.pipeline.writing_pipeline import write_new_chapter

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


@cli.group()
def generate():
    """Generate settings (world, character, outline)."""
    pass

@generate.command("world")
@click.argument("project_id")
@click.option("--prompt", default="", help="Prompt for worldbuilding")
def gen_world(project_id: str, prompt: str):
    """Generate worldbuilding settings."""
    click.echo("Generating worldbuilding...")
    res = asyncio.run(generate_worldbuilding(project_id, prompt))
    click.secho(f"✅ Generated worldbuilding:\n{res}", fg="green")

@generate.command("character")
@click.argument("project_id")
@click.option("--prompt", default="", help="Prompt for characters")
def gen_character(project_id: str, prompt: str):
    """Generate character settings."""
    click.echo("Generating characters...")
    res = asyncio.run(generate_characters(project_id, prompt))
    click.secho(f"✅ Generated characters:\n{res}", fg="green")

@generate.command("outline")
@click.argument("project_id")
def gen_outline(project_id: str):
    """Generate novel outline."""
    click.echo("Generating outline...")
    res = asyncio.run(generate_outline(project_id))
    click.secho(f"✅ Generated outline:\n{res}", fg="green")

@cli.group()
def write():
    """Write chapter content."""
    pass

@write.command("new")
@click.argument("project_id")
@click.argument("chapter_id")
@click.option("--prompt", default="", help="Directions for the chapter")
def write_new(project_id: str, chapter_id: str, prompt: str):
    """Write a new chapter."""
    click.echo(f"Writing Chapter {chapter_id}...")
    res = asyncio.run(write_new_chapter(project_id, chapter_id, prompt))
    click.secho(f"✅ Chapter written:\n{res[:500]}...", fg="green")

if __name__ == "__main__":
    cli()
