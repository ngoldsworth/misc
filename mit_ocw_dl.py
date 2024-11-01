import bs4
import requests

import urllib.parse
import pathlib as pl

headers = {
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
}

def url_to_file(url, file, verbose=False):
    r = requests.get(url)
    with open(file, 'wb') as f:
        f.write(r.content)
    if verbose:
        print(f'    ({file.stat().st_size >> 10:>10} kb)')

def download_course(
    top_url: str,
    target_dir: pl.Path = pl.Path("./"),
    get_videos=False,
    over_write=False,
    verbose=True,
):
    # top_url = urllib.parse.urlparse(top_url)
    if verbose:
        print(f"downloading course:")
        print(f"    url: {top_url}")
        print(f"    target_dir: {target_dir}")

    dl_url = urllib.parse.urljoin(top_url, "download")
    r = requests.get(dl_url, headers=headers)

    if not target_dir.exists():
        target_dir.mkdir(parents=True)

    if get_videos:
        video_dir = target_dir / "videos"
        if not video_dir.exists():
            video_dir.mkdir(parents=True)

        video_url = top_url + 'resources/lecture-videos/'
        r_vid = requests.get(video_url)
        data = bs4.BeautifulSoup(r_vid.text, "html.parser")
        for l in data.find_all("a"):
            loc_href = l['href']
            x = urllib.parse.urlparse(loc_href)
            if x.netloc == "":
                p_dl_url = urllib.parse.urlparse(dl_url)
                k = p_dl_url._replace(path=loc_href)
                childurl = urllib.parse.urlunparse(k)
            else:
                childurl = loc_href
            spl = urllib.parse.urlsplit(childurl)
            path = pl.Path(spl.path)

            is_video = get_videos and path.suffix.lower() == ".mp4"
            if is_video:
                savename = video_dir / path.name
                if over_write or not savename.exists():
                    url_to_file(childurl, savename, verbose=verbose)
                    # r2 = requests.get(childurl, headers=headers)
                    # with open(savename, "wb") as f:
                    #     f.write(r2.content)
                    # if verbose:
                    #     print(f"      ({savename.stat().st_size >> 10:>10}kb) {savename}")
    return

    data = bs4.BeautifulSoup(r.text, "html.parser")
    for l in data.find_all("a"):
        loc_href = l["href"]

        # sometimes href has entire URL, others it doesnt
        x = urllib.parse.urlparse(loc_href)
        if x.netloc == "":
            p_dl_url = urllib.parse.urlparse(dl_url)
            k = p_dl_url._replace(path=loc_href)
            childurl = urllib.parse.urlunparse(k)
        else:
            childurl = loc_href

        spl = urllib.parse.urlsplit(childurl)
        path = pl.Path(spl.path)

        is_zip = path.suffix.lower() == ".zip"
        is_video = get_videos and path.suffix.lower() == ".mp4"


        # if is_zip or is_video:
        #     if is_video:
        #         savename = video_dir / path.name
        #     else:
        #         savename = target_dir / path.name

        #     if over_write or not savename.exists():
        #         r2 = requests.get(childurl, headers=headers)
        #         with open(savename, "wb") as f:
        #             f.write(r2.content)
        #         if verbose:
        #             print(f"      ({savename.stat().st_size >> 10:>10}kb) {savename}")

        #     elif verbose:
        #         print(f"      (already done) {savename}")


if __name__ == "__main__":
    top_dir = pl.Path(r"C:\Users\nelson.goldsworth\Desktop\mit_ocw")
    course_urls = {
        # 'phys_8.701_particle': 'https://ocw.mit.edu/courses/8-701-introduction-to-nuclear-and-particle-physics-fall-2020/',
        "phys_8.421_atomic_optical_1": "https://ocw.mit.edu/courses/8-421-atomic-and-optical-physics-i-spring-2014/",
        "phys_8.421_atomic_optical_1": "https://ocw.mit.edu/courses/8-422-atomic-and-optical-physics-ii-spring-2013/",
        "phys_8.333_statmech_1": "https://ocw.mit.edu/courses/8-333-statistical-mechanics-i-statistical-mechanics-of-particles-fall-2013/",
        "phys_8.334_statmech_2": "https://ocw.mit.edu/courses/8-334-statistical-mechanics-ii-statistical-physics-of-fields-spring-2014/",
        "phys_8.962_general_relativity": "https://ocw.mit.edu/courses/8-962-general-relativity-spring-2020/",
        "phys_8.323_qft_1": "https://ocw.mit.edu/courses/8-323-relativistic-quantum-field-theory-i-spring-2023/",
        "math_18.s190_intro_to_metric_spaces": "https://ocw.mit.edu/courses/18-s190-introduction-to-metric-spaces-january-iap-2023/",
        "math_18.065_matrix_methods_strang": "https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/",
        "math_18.085_computational_sci_eng_1": "https://ocw.mit.edu/courses/18-085-computational-science-and-engineering-i-fall-2008/",
        "math_18.086_computational_sci_eng_2": "https://ocw.mit.edu/courses/18-086-mathematical-methods-for-engineers-ii-spring-2006/",
        "math_18.100A_real_analysis": "https://ocw.mit.edu/courses/18-100a-real-analysis-fall-2020/",
        "math_18.102_functional_analysis": "https://ocw.mit.edu/courses/18-102-introduction-to-functional-analysis-spring-2021/",
        "math_18.225_graph_theory_additive_cominatorics": "https://ocw.mit.edu/courses/18-225-graph-theory-and-additive-combinatorics-fall-2023/",
        # "math_18.s097_applied_category_theory": "https://ocw.mit.edu/courses/18-s097-applied-category-theory-january-iap-2019/",
        "math_18.404j_theory_of_computation": "https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/",
        "eecs_6.003_signals_systems": "https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/",
        "eecs_6.006_intro_algo_2020": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
        "eecs_6.006_intro_algo_2011": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/",
        "eecs_6.042j_math_for_compsci": "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/",
        "eecs_6.046j_intro_algo_2": "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/",
        "eecs_6.046j_design_analysis_algo_sp2015": "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
        "eecs_6.172_performance_engineering_software_systems": "https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/",
        "eecs_6.622_power_electronics": "https://ocw.mit.edu/courses/6-622-power-electronics-spring-2023/",
        "eecs_6.851_advanced_data_structures": "https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/",
        "eecs_RES.6-008_dsp" : "https://ocw.mit.edu/courses/res-6-008-digital-signal-processing-spring-2011/",
        "16.842_fundamentals_of_systems_engineering": "https://ocw.mit.edu/courses/16-842-fundamentals-of-systems-engineering-fall-2015/",
    }

    for course, url in course_urls.items():
        print(f"starting {course}")
        download_course(
            url,
            target_dir=top_dir / course,
            get_videos=True,
            verbose=True,
        )
