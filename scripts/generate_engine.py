import asyncio
import click
from novel.core.memory.context_builder import build_chapter_context
from novel.core.llm.client import generate_text
from novel.core.workflow.qa_loop import run_qa_loop

@click.command()
@click.argument('project_dir')
def run(project_dir):
    async def main():
        print("1. Assembling Context...")
        ctx = build_chapter_context(project_dir)
        print("2. Generating Draft...")
        draft = await generate_text(f"Write chapter 1 based on context:\n{ctx}")
        print("3. Running QA Loop...")
        final = await run_qa_loop(draft, ctx)
        print("\n--- FINAL OUTPUT ---\n")
        print(final)
        print("\n[PAUSED FOR HUMAN IN THE LOOP] You can now use Claude Skills to refine this draft.")
    asyncio.run(main())

if __name__ == '__main__':
    run()
