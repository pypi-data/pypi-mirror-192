import shutil
from pathlib import Path
from typing import Union

from pydantic import Field
from typing_extensions import Annotated

from supertemplater.context import Context
from supertemplater.settings import Settings

from .base import RenderableBaseModel
from .directory_dependency import DirectoryDependency
from .file_dependency import FileDependency
from .git_dependency import GitDependency
from .project_variables import ProjectVariables

ProjectDependency = Annotated[
    Union[GitDependency, FileDependency, DirectoryDependency],
    Field(discriminator="src_type"),
]


class Project(RenderableBaseModel):
    _RENDERABLE_EXCLUDES = {"settings"}

    dependencies: list[ProjectDependency]
    base_dir: Path

    settings: Settings = Settings()
    variables: ProjectVariables = ProjectVariables()

    @property
    def exists(self) -> bool:
        return self.base_dir.exists()

    @property
    def is_empty(self) -> bool:
        if not self.exists:
            return True
        return not any(self.base_dir.iterdir())

    def resolve_dependencies(self, context: Context) -> None:
        self.base_dir.mkdir(exist_ok=True)
        for dependency in self.dependencies:
            dependency.resolve(self.base_dir, context)

    def empty(self) -> None:
        if self.exists:
            shutil.rmtree(self.base_dir)
