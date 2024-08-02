from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import subprocess
import os

class GenerateProtoCommand(build_py):
    """Custom build command to generate gRPC Python code from .proto files."""

    def run(self):
        # Generate gRPC Python code
        proto_files = [
            'hello_world.proto'
        ]
        proto_dir = 'main/testgrpc/interface'
        generated_dir = 'main/testgrpc/lib'
        print(f'Proto directory: {proto_dir}')
        print(f'Generated directory: {generated_dir}')
        for proto_file in proto_files:
            proto_path = os.path.join(proto_dir, proto_file)
            print(f'Generating gRPC Python code for {proto_path}')
            subprocess.check_call([
                'python', '-m', 'grpc_tools.protoc',
                f'--proto_path={proto_dir}',
                f'--python_out={generated_dir}',
                f'--grpc_python_out={generated_dir}',
                proto_path,
            ])

        # Call parent build command
        build_py.run(self)

setup(
    name='libgrpc',
    version='0.1.0',
    packages=find_packages("main", exclude=["api","api.models"]),
    package_dir={"testgrpc":"main/testgrpc"},

    install_requires=[
        'grpcio>=1.51.1',
        'grpcio-tools>=1.51.1',
    ],
    cmdclass={
        'build_py': GenerateProtoCommand,
    },
    include_package_data=True
)