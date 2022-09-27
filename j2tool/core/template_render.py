
import json
import os
import jinja2
from j2tool.app import applogging
import yaml
from j2tool.cross import serialization

from j2tool.cross.helpers import ensure_dir

import re
CONTEXT_ID = "j2r_context"


class SegmentCode():
    def __init__(self, id, content, ident):
        self.id = id
        self.content = content
        self.ident = ident


class Solution():
    def __init__(self,
                 solution_dir,
                 output_dir,
                 template_dir,
                 var_file_dirs=[],
                 var_files=[]) -> None:
        self.solution_dir = solution_dir
        self.output_dir = output_dir
        self.template_dir = template_dir
        self.var_file_dirs = var_file_dirs
        self.var_files = var_files
        self.main_template = "main.j2"

    def get_template_dir(self):
        return self.template_dir

    def get_main_template(self):
        result = self.main_template
        return result

    def get_manifest_path(self):
        return ".j2tool.out"


class RenderCache():
    def __init__(self) -> None:
        self.cache_dir = ".j2t_cache"

    def update_file_data(self, path: str, data: dict):
        cache_path = os.path.join(self.cache_dir, f"{path}.json")
        # if not os.path.exists(cache_path):
        #     ensure_dir(cache_path)
        #     with

        if os.path.exists(cache_path):
            with open(cache_path, "r") as rfile:
                prev_data: dict = json.load(
                    rfile, object_hook=serialization.dict_to_obj)
                prev_data.update(data)
                data = prev_data
        else:
            ensure_dir(cache_path)

        with open(cache_path, "w") as file:
            json.dump(data, file, default=serialization.convert_to_dict,
                      indent=4, sort_keys=True)

        return data


class RenderContext():
    def __init__(self, solution: Solution) -> None:
        self.solution = solution
        self.file_paths = []
        self.rcache = RenderCache()

    def get_solution(self):
        return self.solution

    def add_file(self, file_path):
        norm_file_path = os.path.normpath(file_path)

        if not norm_file_path in self.file_paths:
            self.file_paths.append(norm_file_path)

    def get_file_paths(self) -> list[str]:
        return self.file_paths

    def get_rcache(self) -> RenderCache:
        return self.rcache


logger = applogging.LogManager().get_app_logger()


def get_placeholder_data(content: str):
    result = {}
    # Extract all identified segments
    regex = r"^(?P<ident>[ \t]*)# # ## j2t_begin_block (?P<id>.*)\n(?P<content>(.|\n)*?)^([ \t]*)# # ## j2t_end_block (?P<id2>.*)\n"
    matches = re.finditer(regex, content, re.MULTILINE)

    for matchNum, match in reversed(list(enumerate(matches, start=1))):
        logger.debug("Match {matchNum} was found at {start}-{end}: {match}".format(
            matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()))

        id = match.group("id")
        ident = match.group("ident")
        groups = match.groups()
        content = match.group("content")
        start = match.start("content")
        end = match.end("content")

        if id in result:
            logger.warn(f"The key {id} already exists")

        result[id] = SegmentCode(id, content, ident)

    return result


def set_placeholder_data(content: str, data: dict):

    # Extract all identified segments
    regex = r"^(?P<ident>[ \t]*)# # ## j2t_begin_block (?P<id>.*)\n(?P<content>(.|\n)*?)^([ \t]*)# # ## j2t_end_block (?P<id2>.*)\n"
    matches = re.finditer(regex, content, re.MULTILINE)

    expand_content = content

    for matchNum, match in reversed(list(enumerate(matches, start=1))):
        logger.debug("Match {matchNum} was found at {start}-{end}: {match}".format(
            matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()))

        id = match.group("id")
        ident = match.group("ident")
        groups = match.groups()
        content = match.group("content")
        start = match.start("content")
        end = match.end("content")

        if id in data:
            segment_code: SegmentCode = data[id]

            expand_content1 = expand_content[0:start] + segment_code.content + \
                "\n" + expand_content[end:len(expand_content)]
            expand_content = expand_content1

    return expand_content


def j2r_generate(renderCxt: RenderContext, model, template_path, file_path):

    solution: Solution = renderCxt.get_solution()
    template = create_template(renderCxt, template_path)

    rendered_content = template.render(model=model)

    result = ""

    if file_path:
        output_file_path = os.path.normpath(
            os.path.join(solution.output_dir, file_path))
        ensure_dir(output_file_path)

        if os.path.exists(output_file_path):
            with open(output_file_path) as file:
                content = file.read()
            place_holders = get_placeholder_data(content)
            data = renderCxt.get_rcache().update_file_data(file_path, place_holders)
            rendered_content = set_placeholder_data(rendered_content, data)

        renderCxt.add_file(output_file_path)

        with open(output_file_path, "w") as file:
            file.write(rendered_content)

        result = output_file_path

    return result


def create_template(context: RenderContext, template_path):

    template_dir = context.get_solution().get_template_dir()
    templateLoader = jinja2.FileSystemLoader(template_dir)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_path)

    context_dict = {
        "j2r_generate": j2r_generate,
        "j2r_context": context
    }

    template.globals.update(context_dict)
    return template


def load_manifest(manifest_path: str) -> list[str]:
    file_paths = []
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as file:
            file_paths = json.load(file)
    return file_paths


def clean_files(file_paths: list[str]):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)


def save_manifest(manifest_path: str, file_paths):
    with open(manifest_path, "w") as file:
        json.dump(file_paths, file)


def render(solution: Solution, model: dict):
    try:
        manifest_path = os.path.join(
            solution.output_dir, solution.get_manifest_path())
        file_paths: list[str] = load_manifest(manifest_path)

        renderContext = RenderContext(solution)
        main_template_path = solution.get_main_template()
        template = create_template(renderContext, main_template_path)
        # this is where to put args to the template renderer
        outputText = template.render(model=model)

        new_file_paths: list[str] = renderContext.get_file_paths()
        save_manifest(manifest_path, new_file_paths)

        if file_paths:
            pending_file_paths = set(file_paths) - set(new_file_paths)
            clean_files(list(pending_file_paths))

        logger.info(f"Render: {outputText}")

    except:
        logger.exception("ERROR ")
