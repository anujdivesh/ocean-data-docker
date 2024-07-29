
class PathManager:
    # Hardcoded URL paths
    #base_dir = "/home/pop/Desktop/ocean-portal2.0/backend_design"
    base_dir = "/scripts"
    datasets = "/home/pop/ocean_portal/datasets"
    URLS = {
        'ocean-api': 'https://dev-oceanportal.spc.int/v1/api',
        'tmp': base_dir+'/tmp',
        'odbaac': base_dir,
        'copernicus-credentials': base_dir+'/.copernicusmarine/.copernicusmarine-credentials',
        'root-dir': datasets
    }

    @classmethod
    def get_url(cls, key, *args):
        """Constructs a URL by joining the specified base URL with the provided arguments."""
        if key not in cls.URLS:
            raise ValueError(f"Invalid key '{key}'. Available keys: {list(cls.URLS.keys())}")
        return "/".join([cls.URLS[key]] + list(args))

