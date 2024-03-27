__all__ = ["get_entry_points"]

# import entry_points from importlib.metadata or fall back to pkg_resources
# TODO: add importlib_metadata as another option
try:
    from importlib.metadata import entry_points

    def get_entry_points(group):
        return entry_points(group=group)

except ImportError:
    import pkg_resources

    def get_entry_points(group):
        return pkg_resources.iter_entry_points(group)
