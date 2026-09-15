"""Page content for the BDAL powerlifting viva guide.

code_block, shell and hbar are injected by build.py before sections() runs.
Every number here was checked against the project results or recomputed from the CSV.
"""

code_block = shell = hbar = None  # injected

HERO = """
<header class="hero">
  <h1>OpenPowerlifting on Hadoop: the viva guide</h1>
  <p>Big Data Analytics Lab (CSE 4346) final project. Read this before the viva and the quiz. It covers the
  dataset, how we built the cluster, the Hadoop, MapReduce and Pig theory, every line of our code, the terminal
  commands the examiner may ask you to type, and self-tests.</p>
  <div class="chips">
    <span class="chip">4,030,219 rows · 42 columns · 785.5 MB</span>
    <span class="chip">Hadoop 3.4.1 · Pig 0.17.0 · Java 11</span>
    <span class="chip">3 MapReduce jobs + 5 Pig scripts</span>
    <span class="chip">8 / 8 outputs verified</span>
  </div>
</header>
"""

ARROW_DEF = ('<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
             'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor" style="fill:var(--muted)"/></marker></defs>')


def svg(w, h, inner, cap=None, label="diagram"):
    c = f'<div class="cap">{cap}</div>' if cap else ""
    return (f'<div class="figwrap"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f'{ARROW_DEF}{inner}</svg>{c}</div>')


def box(x, y, w, h, cls, lines, mono=False):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="{cls}"/>']
    n = len(lines)
    for i, ln in enumerate(lines):
        ty = y + h / 2 + (i - (n - 1) / 2) * 16 + 4
        klass = "t-b" if i == 0 else "t-s"
        if mono and i > 0:
            klass += " t-m"
        out.append(f'<text x="{x + w / 2}" y="{ty:.1f}" text-anchor="middle" class="{klass}">{ln}</text>')
    return "".join(out)


def arrow(x1, y1, x2, y2):
    return f'<path d="M{x1},{y1} L{x2},{y2}" class="ar"/>'


def table(head, rows, num=()):
    th = "".join(f'<th class="{"num" if i in num else ""}">{h}</th>' for i, h in enumerate(head))
    trs = "".join("<tr>" + "".join(f'<td class="{"num" if i in num else ""}">{c}</td>' for i, c in enumerate(r))
                  + "</tr>" for r in rows)
    return f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def qa(tag, q, a):
    return f'<details class="qa" data-tag="{tag}"><summary>{q}<span class="tag">{tag}</span></summary><div class="a">{a}</div></details>'


# ============================================================ sections
def s_start():
    return """
<h2><small>Start here</small>The 60-second version</h2>
<p>If the examiner says "explain your project", say this, in this order.</p>
<div class="box say"><b>Say it like this</b>
We analysed the OpenPowerlifting archive, a public-domain CSV of about four million powerlifting competition
entries, 785 MB with 42 columns. We ran a single-node Hadoop 3.4.1 cluster with HDFS and YARN, put the CSV into
HDFS, and answered eight questions: three with Java MapReduce jobs and five with Pig Latin scripts. The
MapReduce jobs use three design patterns: finding a maximum inside the mapper, a min/max/count/average
summary with a custom Writable and a combiner, and counting with the reducer reused as the combiner. Every
result was checked against an independent awk calculation straight from the CSV, and all eight matched.</div>
<h3>Numbers you must know cold</h3>
<div class="grid2">
  <div class="stat"><div class="v">4,030,219</div><div class="k">data rows (plus 1 header row)</div></div>
  <div class="stat"><div class="v">42</div><div class="k">columns, indexed $0 to $41</div></div>
  <div class="stat"><div class="v">785.5 MB</div><div class="k">CSV size in HDFS (823,619,397 bytes)</div></div>
  <div class="stat"><div class="v">7</div><div class="k">HDFS blocks at 128 MB each, so 7 map tasks</div></div>
  <div class="stat"><div class="v">1407.5 kg</div><div class="k">highest total: Dave Hoff, Multi-ply, 2019-10-28</div></div>
  <div class="stat"><div class="v">818.06</div><div class="k">highest Dots: Deana Tollefson</div></div>
  <div class="stat"><div class="v">535,620</div><div class="k">entries for THSPA, the busiest federation</div></div>
  <div class="stat"><div class="v">475</div><div class="k">distinct federations</div></div>
  <div class="stat"><div class="v">6</div><div class="k">daemons: NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager, JobHistoryServer</div></div>
  <div class="stat"><div class="v">1</div><div class="k">replication factor (dfs.replication) on our single node</div></div>
</div>
""" + svg(860, 250, "".join([
        box(10, 80, 130, 80, "bxw", ["CSV file", "785.5 MB", "4.03 M rows"]),
        arrow(140, 120, 185, 120),
        box(188, 80, 140, 80, "bxa", ["HDFS", "/powerlifting/", "7 blocks"]),
        arrow(328, 105, 380, 55), arrow(328, 135, 380, 185),
        box(383, 20, 170, 70, "bxg", ["3 MapReduce jobs", "Java, run by YARN"]),
        box(383, 150, 170, 70, "bxv", ["5 Pig scripts", "compiled to MR jobs"]),
        arrow(553, 55, 600, 105), arrow(553, 185, 600, 135),
        box(603, 80, 110, 80, "bxa", ["Output", "part-r-00000", "in HDFS"]),
        arrow(713, 120, 745, 120),
        box(748, 80, 104, 80, "bxg", ["diff vs", "awk ground", "truth ✓"]),
    ]), "The whole project on one line: data into HDFS, two processing engines, outputs checked against an independent calculation.", "project pipeline")


def s_journey():
    return """
<h2><small>How we did it</small>From an empty laptop to verified results</h2>
<p>This is the order we actually worked in. The examiner may ask "how did you set this up?" or "what problems did you face?", so know each step.</p>
<ol class="steps">
<li><b>Learned the basics in the lab sessions</b>Lab 1 was Hadoop installation and configuration. Lab 2 was HDFS commands (<code>mkdir</code>, <code>put</code>, <code>ls</code>, <code>cat</code>). Lab 3 was a MapReduce program (matrix multiplication). The project reuses exactly those skills on a real dataset.</li>
<li><b>Chose a real, large dataset</b>We picked the OpenPowerlifting bulk CSV because it is genuinely big (4 million rows, 785 MB), free to use (public domain), and has clear numeric columns to aggregate. We downloaded the zip (about 170 MB) and unzipped the 2026-09-05 snapshot.</li>
<li><b>Explored it before writing any code</b>We printed the header to get the column positions (<code>head -1 file.csv | tr ',' '\\n' | cat -n</code>), and checked with awk that every row has exactly 42 fields. It does, and no field contains a comma or a quote, so a plain <code>split(",")</code> is safe.</li>
<li><b>Installed the software</b>OpenJDK 11 (Hadoop 3.4 runs on Java 8 or 11, not 17), the Hadoop 3.4.1 and Pig 0.17.0 tarballs extracted into <code>~/bigdata</code>, and an env file that sets <code>JAVA_HOME</code>, <code>HADOOP_HOME</code>, <code>PIG_HOME</code> and <code>PATH</code>.</li>
<li><b>Set up passwordless SSH to localhost</b><code>start-dfs.sh</code> and <code>start-yarn.sh</code> start each daemon over SSH, even on one machine, so we generated a key and added it to <code>authorized_keys</code>.</li>
<li><b>Configured four XML files</b><code>core-site.xml</code>, <code>hdfs-site.xml</code>, <code>mapred-site.xml</code> and <code>yarn-site.xml</code> (details in the Hadoop section below).</li>
<li><b>Formatted the NameNode once, then started the cluster</b><code>hdfs namenode -format</code> creates an empty filesystem. Then <code>start-dfs.sh</code>, <code>start-yarn.sh</code>, <code>mapred --daemon start historyserver</code>, and <code>jps</code> to see the six daemons.</li>
<li><b>Put the data into HDFS</b><code>hdfs dfs -mkdir -p /powerlifting</code> and <code>hdfs dfs -put</code> the CSV as <code>/powerlifting/openpowerlifting.csv</code>. HDFS split it into 7 blocks.</li>
<li><b>Wrote, compiled and ran the MapReduce jobs</b>Three Java programs, each with a Mapper, a Reducer and a Driver. Compiled with <code>javac -cp "$(hadoop classpath)"</code>, packed with <code>jar cf</code>, and run with <code>hadoop jar</code>.</li>
<li><b>Wrote and ran the Pig scripts</b>Five <code>.pig</code> files, run with <code>pig -x mapreduce -f script.pig</code>. Pig turned each one into MapReduce jobs on the same cluster.</li>
<li><b>Verified every number</b>A separate awk script computed all eight answers straight from the CSV, with no Hadoop involved. Every cluster result matched. MR3 and Pig 1 answer the same question, so they also check each other.</li>
<li><b>Wrote the report, then rebuilt everything once more</b>The laptop was reinstalled on 2026-09-05, so we rebuilt the cluster from scratch, downloaded the newest snapshot and re-ran all eight jobs. All numbers were re-verified. That is a good answer to "is this reproducible?"</li>
</ol>
<h3>Problems we hit and how we fixed them</h3>
""" + table(["Problem", "Cause", "Fix"], [
        ["Hadoop would not run on a newer Java", "Hadoop 3.4.x supports Java 8 and 11 only", "Installed OpenJDK 11 and set <code>JAVA_HOME</code> to it"],
        ["SecondaryNameNode did not start", "Its address defaults to <code>0.0.0.0</code>, so the start script used SSH to the machine's hostname, but our SSH server only listens on localhost", "Set <code>dfs.namenode.secondary.http-address</code> to <code>localhost:9868</code> in hdfs-site.xml"],
        ["<code>FileAlreadyExistsException</code> when re-running a job", "Hadoop refuses to write into an output directory that already exists", "Delete it first: <code>hdfs dfs -rm -r -f /powerlifting/out_toptotal</code>"],
        ["A top-level <code>ORDER BY</code> in Pig failed", "Known issue with Pig 0.17 running on Hadoop 3", "Sort inside a nested block: <code>FOREACH (GROUP ...) { ORDER ...; LIMIT ...; }</code>"],
        ["<code>jps</code> showed 5 daemons instead of 6", "NodeManager takes a few seconds to start", "Run <code>hdfs dfsadmin -safemode wait</code> first, then <code>jps</code>"],
        ["<code>hdfs dfs -cat out/part-*</code> said no such file", "The local shell tried to expand <code>*</code> as a local filename", "Quote HDFS globs: <code>'Top10Dots.txt/part-*'</code>"],
    ])


def s_dataset():
    eq_all = [("Raw", 1918876), ("Single-ply", 1414999), ("Unlimited", 324270), ("Wraps", 240815), ("Multi-ply", 131140), ("Straps", 119)]
    events = [("SBD (full meet)", 2910932), ("B (bench only)", 798593), ("D (deadlift only)", 218503), ("BD", 75657), ("S", 19938), ("SB", 4185), ("SD", 2411)]
    feds = [("THSPA", 535620), ("USAPL", 365199), ("THSWPA", 325029), ("USPA", 232091), ("FPR", 191693), ("USPF", 153472), ("CPU", 70177), ("APF", 65017), ("WPC-RUS", 64946), ("WRPF", 61516)]
    cols = ["Name", "Sex", "Event", "Equipment", "Age", "AgeClass", "BirthYearClass", "Division", "BodyweightKg", "WeightClassKg",
            "Squat1Kg", "Squat2Kg", "Squat3Kg", "Squat4Kg", "Best3SquatKg", "Bench1Kg", "Bench2Kg", "Bench3Kg", "Bench4Kg", "Best3BenchKg",
            "Deadlift1Kg", "Deadlift2Kg", "Deadlift3Kg", "Deadlift4Kg", "Best3DeadliftKg", "TotalKg", "Place", "Dots", "Wilks", "Glossbrenner",
            "Goodlift", "Tested", "Country", "State", "Federation", "ParentFederation", "Date", "MeetCountry", "MeetState", "MeetTown", "MeetName", "Sanctioned"]
    used = {0, 1, 3, 25, 27, 34, 36}
    colgrid = "".join(f'<span class="chip" style="{"background:var(--accent);color:var(--accent-ink);border-color:var(--accent)" if i in used else ""}">${i} {c}</span>' for i, c in enumerate(cols))
    return f"""
<h2><small>The data</small>The OpenPowerlifting dataset</h2>
<p><b>OpenPowerlifting</b> is a volunteer project that records the results of powerlifting competitions around
the world. It publishes the whole archive as one CSV file. We used the snapshot dated <b>2026-09-05</b>, file
<code>openpowerlifting-2026-09-05-b8b9bf6e.csv</code>.</p>
""" + table(["Fact", "Value"], [
        ["Source", "openpowerlifting.org, bulk CSV download (<code>openpowerlifting-latest.zip</code>)"],
        ["Licence", "Public domain. The project waives copyright; it only asks for attribution."],
        ["Format", "One CSV file, comma separated, one header row"],
        ["Size", "823,619,397 bytes = 785.5 MB (as HDFS shows it). About 170 MB zipped."],
        ["Rows", "4,030,219 data rows + 1 header (<code>wc -l</code> prints 4,030,220)"],
        ["Columns", "42, indexed <code>$0</code> to <code>$41</code>"],
        ["Date range", "1964-09-05 to 2026-08-30"],
        ["Distinct names", "1,012,540 (same-name lifters get a <code>#N</code> suffix, like <code>Dave Hoff #1</code>)"],
        ["Federations", "475 distinct values in the Federation column"],
        ["Meet countries", "133 distinct values in MeetCountry"],
        ["Quirks", "No commas or quotes inside fields, so a plain split works. Some metric fields are empty."],
    ]) + f"""
<h3>What one row means</h3>
<p>One row is <b>one lifter's result at one competition</b>. A lifter who competed six times has six rows. So
"4 million rows" means 4 million competition entries, not 4 million people.</p>
<h3>All 42 columns (the 7 we use are highlighted)</h3>
<div class="chips">{colgrid}</div>
""" + table(["Column", "Index", "Type", "Meaning", "Used by"], [
        ["Name", "<code>$0</code>", "text", "lifter name, with <code>#N</code> if names clash", "MR1, Pig 2–5, header filter"],
        ["Sex", "<code>$1</code>", "text", "M, F or Mx", "Pig 4, Pig 5"],
        ["Equipment", "<code>$3</code>", "text", "Raw, Wraps, Single-ply, Multi-ply, Unlimited, Straps", "MR1, MR2, Pig 2, Pig 3"],
        ["TotalKg", "<code>$25</code>", "number", "best squat + best bench + best deadlift, in kg", "MR1, MR2, Pig 2, Pig 3"],
        ["Dots", "<code>$27</code>", "number", "strength score adjusted for bodyweight", "Pig 4, Pig 5"],
        ["Federation", "<code>$34</code>", "text", "organisation that ran the meet", "MR3, Pig 1"],
        ["Date", "<code>$36</code>", "date", "competition date", "MR1 (printed in the result)"],
    ]) + """
<div class="box trap"><b>Trap: 0-based indexes</b>Pig's <code>$25</code> and Java's <code>f[25]</code> are the
<b>26th</b> column. <code>cat -n</code> numbers from 1, so it prints TotalKg as line 26. If asked "which column is
TotalKg?", say "index 25, the 26th column".</div>
<h3>Total vs Dots</h3>
<p><b>TotalKg</b> is the sport's headline number: the sum of the best successful squat, bench press and deadlift.
Heavier lifters lift more, so the total rewards absolute strength.</p>
<p><b>Dots</b> makes lifters of different bodyweights comparable. It scales the total by a polynomial of
bodyweight:</p>
<div class="box deep"><b>The formula</b>
<code>Dots = TotalKg × 500 / (a + b·W + c·W² + d·W³ + e·W⁴)</code>, where W is bodyweight in kg (clamped to
40–210 kg for men, 40–150 kg for women), with separate coefficients for men and women. We checked this against
2,000 rows of the dataset and every computed value matched the Dots column to within 0.005.
</div>
<p>That is why the Dots top 10 is mostly women, while the total top 10 is all heavy men.</p>
<h3>Equipment categories</h3>
""" + table(["Category", "Meaning", "Rows in file"], [
        ["Raw", "belt and sleeves only", "1,918,876"],
        ["Single-ply", "one-layer supportive suit and shirt", "1,414,999"],
        ["Unlimited", "no equipment limits", "324,270"],
        ["Wraps", "raw plus knee wraps (helps the squat)", "240,815"],
        ["Multi-ply", "multi-layer suits, the most support; holds the all-time total record", "131,140"],
        ["Straps", "deadlift with straps, a tiny group", "119"],
    ], num=(2,)) + hbar("Rows per equipment category (all 4,030,219 rows)", eq_all) + """
<h3>Events, sex and missing values</h3>
<p>The Event column says which lifts were contested. <b>SBD</b> means squat, bench and deadlift (a full meet).
<b>B</b> is bench only, so for those rows the "total" is just the bench press.</p>
""" + hbar("Rows per event type", events) + table(["Sex", "Rows"], [["M", "2,903,501"], ["F", "1,126,519"], ["Mx", "199"]], num=(1,)) + """
<p><b>Missing values:</b> 270,254 rows have an empty TotalKg and 296,478 have an empty Dots. This happens when a
lifter fails all attempts at a lift ("bombs out") or when bodyweight is unknown. Our jobs skip empty values, so
MR2 counts 3,759,965 rows with a total (4,030,219 − 270,254).</p>
<h3>Federations</h3>
""" + hbar("Top 10 federations by entries (MR3 result)", feds) + """
<p>The surprise: <b>THSPA</b> (Texas High School Powerlifting Association) and <b>THSWPA</b> (Texas High School
Women's Powerlifting Association) have more entries than any national federation. High-school meets are
frequent, large and well recorded. USAPL (USA Powerlifting) and USPA (United States Powerlifting Association)
are the biggest national ones.</p>
"""


def s_hadoop():
    return """
<h2><small>Theory 1</small>Hadoop: HDFS and YARN</h2>
<p>Hadoop has two main parts. <b>HDFS</b> stores the data. <b>YARN</b> runs the programs. MapReduce and Pig are
programs that run on YARN and read from HDFS.</p>
""" + svg(860, 330, "".join([
        '<text x="215" y="22" text-anchor="middle" class="t-b">HDFS: storage</text>',
        '<text x="645" y="22" text-anchor="middle" class="t-b">YARN: compute</text>',
        box(20, 40, 390, 80, "bxa", ["NameNode  (port 9870 web UI)", "the index: file names, blocks, which DataNode holds each block"]),
        box(20, 140, 180, 80, "bxa", ["DataNode", "stores the actual", "block data on disk"]),
        box(230, 140, 180, 80, "bx", ["SecondaryNameNode", "checkpoints metadata", "NOT a backup (port 9868)"]),
        box(450, 40, 390, 80, "bxg", ["ResourceManager  (port 8088 web UI)", "accepts jobs, hands out containers"]),
        box(450, 140, 180, 80, "bxg", ["NodeManager", "runs containers:", "map and reduce tasks"]),
        box(660, 140, 180, 80, "bx", ["JobHistoryServer", "keeps finished job logs", "(port 19888)"]),
        arrow(110, 120, 110, 138), arrow(540, 120, 540, 138),
        box(20, 250, 820, 60, "bxw", ["One laptop runs all six daemons (pseudo-distributed mode)", "the CSV: 7 blocks × 128 MB each, replication factor 1, fs.defaultFS = hdfs://localhost:9000"]),
    ]), "The six Java processes that <code>jps</code> shows, and what each one does.", "hadoop daemons") + """
<h3>HDFS in five facts</h3>
<ul>
<li><b>Blocks:</b> files are cut into fixed-size blocks, 128 MB by default. Our 785.5 MB CSV became <b>7 blocks</b> (6 full ones and a 17.5 MB remainder).</li>
<li><b>NameNode</b> keeps only metadata in memory: the directory tree and which blocks make up each file. It never stores the data itself.</li>
<li><b>DataNode</b> stores the blocks on local disk and reports to the NameNode with heartbeats.</li>
<li><b>Replication:</b> normally 3 copies of each block. We set <code>dfs.replication</code> to <b>1</b> because a single machine has only one DataNode.</li>
<li><b>Write once, read many:</b> HDFS is built for large sequential reads, which is exactly what a MapReduce scan needs.</li>
</ul>
<div class="box trap"><b>Trap: SecondaryNameNode</b>It is <b>not</b> a standby or backup NameNode. It periodically merges
the NameNode's edit log into a new fsimage (a checkpoint), so restarts are faster and the edit log does not grow forever.</div>
<h3>YARN in four facts</h3>
<ul>
<li><b>ResourceManager</b>: one per cluster. Accepts job submissions and decides where containers run.</li>
<li><b>NodeManager</b>: one per machine. Launches containers (JVMs) that run the map and reduce tasks.</li>
<li><b>ApplicationMaster</b>: started for each job inside a container. It asks the ResourceManager for containers and tracks the job's tasks.</li>
<li><b>Container</b>: a slice of memory and CPU on a node. Each map or reduce task runs in one.</li>
</ul>
<h3>Our four configuration files</h3>
""" + table(["File", "Property", "Our value", "Why"], [
        ["core-site.xml", "<code>fs.defaultFS</code>", "<code>hdfs://localhost:9000</code>", "where clients find the NameNode, so <code>/powerlifting</code> means HDFS"],
        ["core-site.xml", "<code>hadoop.tmp.dir</code>", "<code>~/bigdata/hdfs/tmp</code>", "base directory for temporary files"],
        ["hdfs-site.xml", "<code>dfs.replication</code>", "<code>1</code>", "only one DataNode, so only one copy is possible"],
        ["hdfs-site.xml", "<code>dfs.namenode.name.dir</code>", "<code>~/bigdata/hdfs/namenode</code>", "where the NameNode keeps its metadata"],
        ["hdfs-site.xml", "<code>dfs.datanode.data.dir</code>", "<code>~/bigdata/hdfs/datanode</code>", "where block data is written"],
        ["hdfs-site.xml", "<code>dfs.namenode.secondary.http-address</code>", "<code>localhost:9868</code>", "keeps the SecondaryNameNode on localhost (our SSH fix)"],
        ["mapred-site.xml", "<code>mapreduce.framework.name</code>", "<code>yarn</code>", "run MapReduce jobs on YARN, not in local mode"],
        ["yarn-site.xml", "<code>yarn.nodemanager.aux-services</code>", "<code>mapreduce_shuffle</code>", "enables the shuffle service that moves map output to reducers"],
    ]) + """
<h3>Web interfaces</h3>
""" + table(["UI", "URL", "What to show"], [
        ["NameNode", "http://localhost:9870", "cluster summary, Utilities → Browse the file system → /powerlifting"],
        ["YARN ResourceManager", "http://localhost:8088", "applications: RUNNING → FINISHED, SUCCEEDED"],
        ["JobHistory", "http://localhost:19888", "counters and logs of finished MapReduce jobs"],
    ])


def s_mrtheory():
    return """
<h2><small>Theory 2</small>How a MapReduce job runs</h2>
<p>MapReduce splits a job into two functions you write, <b>map</b> and <b>reduce</b>. Hadoop does everything
in between: splitting the input, running tasks in parallel, and moving and sorting the intermediate data.</p>
""" + svg(860, 300, "".join([
        box(10, 40, 110, 220, "bxw", ["Input", "7 splits", "(one per", "HDFS block)"]),
        arrow(120, 90, 150, 90), arrow(120, 150, 150, 150), arrow(120, 210, 150, 210),
        box(153, 65, 120, 50, "bxa", ["Map task 1"]), box(153, 125, 120, 50, "bxa", ["Map task 2"]), box(153, 185, 120, 50, "bxa", ["… task 7"]),
        arrow(273, 90, 300, 90), arrow(273, 150, 300, 150), arrow(273, 210, 300, 210),
        box(303, 65, 110, 50, "bx", ["Combiner", "(optional)"]), box(303, 125, 110, 50, "bx", ["Combiner"]), box(303, 185, 110, 50, "bx", ["Combiner"]),
        arrow(413, 90, 450, 140), arrow(413, 150, 450, 150), arrow(413, 210, 450, 160),
        box(453, 95, 150, 110, "bxv", ["Shuffle + sort", "partition by key", "sort keys", "group values"]),
        arrow(603, 150, 640, 150),
        box(643, 105, 110, 90, "bxg", ["Reduce task", "one call per", "key"]),
        arrow(753, 150, 780, 150),
        box(783, 105, 70, 90, "bxw", ["Output", "part-r-", "00000"]),
        '<text x="213" y="30" text-anchor="middle" class="t-s">(key, value) pairs</text>',
        '<text x="528" y="30" text-anchor="middle" class="t-s">the expensive, network step</text>',
    ]), "Data flow of every job on this page. The shuffle moves data between tasks, so the less the mappers send, the faster the job.", "mapreduce flow") + table(["Stage", "What happens", "In our jobs"], [
        ["Input split", "The input file is divided into splits, normally one per HDFS block.", "7 splits, so 7 map tasks"],
        ["RecordReader", "<code>TextInputFormat</code> turns a split into records: key = byte offset (<code>LongWritable</code>), value = the line (<code>Text</code>). A line that crosses a block boundary is still read whole.", "every mapper receives <code>(LongWritable, Text)</code>"],
        ["Map", "Your <code>map()</code> is called once per record and may emit any number of (key, value) pairs.", "we split the CSV line and emit one pair (or nothing)"],
        ["Combiner", "An optional mini-reduce on each map task's output, before the shuffle. Hadoop may run it zero, one or many times.", "MR2 and MR3 use one"],
        ["Partition", "Decides which reducer gets each key. Default <code>HashPartitioner</code>: hash(key) mod number of reducers.", "1 reducer, so everything goes to it"],
        ["Shuffle + sort", "Map output is copied to reducers and sorted by key, and values with the same key are grouped.", "why MR3's output is alphabetical by federation"],
        ["Reduce", "Your <code>reduce(key, values)</code> is called once per distinct key.", "sum, merge, or pick the maximum"],
        ["Output", "Each reducer writes one file, <code>part-r-00000</code>, <code>part-r-00001</code>, …, plus an empty <code>_SUCCESS</code> marker.", "one <code>part-r-00000</code> per job"],
    ]) + """
<h3>Key ideas the examiner likes</h3>
<ul>
<li><b>Writable:</b> Hadoop's own compact binary serialization. Keys and values must implement it (<code>Text</code>, <code>LongWritable</code>, <code>IntWritable</code>, or your own class). Keys also need to be comparable (<code>WritableComparable</code>) so they can be sorted.</li>
<li><b>Data locality:</b> YARN tries to run a map task on the node that holds its block, moving code to the data instead of data to the code.</li>
<li><b>When a combiner is allowed:</b> the operation must be associative and commutative (sum, count, min, max), and its input and output types must both equal the map output types. Average is not allowed directly.</li>
<li><b>Output directory:</b> it must not exist before the job starts, so a finished result can never be overwritten by accident.</li>
<li><b>Driver:</b> the <code>main()</code> that builds a <code>Job</code>: which jar, mapper, combiner, reducer, output types, input and output paths, then <code>waitForCompletion(true)</code>.</li>
</ul>
"""


def s_mr1():
    return """
<h2><small>MapReduce job 1</small>TopTotal: the highest total ever lifted</h2>
<p><b>Question:</b> what is the single heaviest TotalKg in the archive, and who lifted it?<br>
<b>Pattern:</b> top-record filtering with in-mapper combining. <b>Result:</b>
<code>Highest TotalKg  Dave Hoff #1  Multi-ply  2019-10-28  1407.5</code></p>
""" + svg(860, 230, "".join([
        box(10, 20, 150, 190, "bxw", ["4,030,219 rows", "in 7 splits"]),
        box(210, 20, 190, 50, "bxa", ["Mapper 1", "keeps its best row only"]),
        box(210, 90, 190, 50, "bxa", ["Mapper 2", "keeps its best row only"]),
        box(210, 160, 190, 50, "bxa", ["… Mapper 7"]),
        arrow(160, 45, 208, 45), arrow(160, 115, 208, 115), arrow(160, 185, 208, 185),
        arrow(400, 45, 470, 105), arrow(400, 115, 470, 115), arrow(400, 185, 470, 125),
        box(473, 70, 170, 90, "bxv", ["7 records", "all with key \"TOP\"", "cross the network"]),
        arrow(643, 115, 680, 115),
        box(683, 70, 170, 90, "bxg", ["1 Reducer", "picks the maximum", "1407.5 kg"]),
    ]), "Instead of shuffling 4 million rows to find one maximum, each mapper sends only its own winner.", "mr1 flow") + """
<h3>Mapper</h3>
""" + code_block("mr/toptotal/src/pl/toptotal/TopTotalMapper.java", [
        ("extends Mapper<LongWritable, Text, Text, Text>", "The four types are input key, input value, output key, output value. Input is (byte offset, line). Output is (Text, Text)."),
        ("private double max = -1;", "Instance fields keep state <b>across</b> <code>map()</code> calls within one map task. Each task has its own Mapper object, so there are 7 separate maxima, one per split."),
        ('split(",", -1)', 'Split the CSV line on commas. The <code>-1</code> keeps trailing empty fields, so a row always has 42 parts even when the last columns are empty.'),
        ("f.length < 42", "Skip three kinds of rows: broken lines (fewer than 42 fields), the header (first field is literally <code>Name</code>), and rows with no total."),
        ("Double.parseDouble(f[25])", "Column 25 is TotalKg. A value that is not a number throws <code>NumberFormatException</code>, which is caught and ignored, so one bad row cannot crash the job."),
        ("if (total > max)", "Keep the best row so far as tab-separated text: name ($0), equipment ($3), date ($36) and total ($25). Strict <code>&gt;</code> means the first row wins a tie."),
        ("protected void cleanup", "<code>cleanup()</code> runs once after the last record of the split. Nothing is written in <code>map()</code>; only here do we emit one pair."),
        ('new Text("TOP")', 'Every mapper uses the same constant key <code>"TOP"</code>, so all 7 candidates land in one reduce group.'),
    ]) + """
<h3>Reducer</h3>
""" + code_block("mr/toptotal/src/pl/toptotal/TopTotalReducer.java", [
        ("extends Reducer<Text, Text, Text, Text>", "Reducer input types must match the mapper output types: (Text, Text)."),
        ("for (Text v : values)", 'Called once for key "TOP" with 7 values, one from each mapper.'),
        ('split("\\t")', "Split the candidate back into its 4 fields. Index 3 is the total."),
        ("if (total > max)", "Keep the largest of the 7 candidates. This is the global maximum."),
        ('new Text("Highest TotalKg")', "Write the answer with a readable key. The output line is <code>Highest TotalKg⇥Dave Hoff #1⇥Multi-ply⇥2019-10-28⇥1407.5</code>."),
    ]) + """
<h3>Driver</h3>
""" + code_block("mr/toptotal/src/pl/toptotal/TopTotalDriver.java", [
        ('Job.getInstance(new Configuration(), "top total lift")', 'Create the job. The name <code>top total lift</code> is what appears in the YARN web UI.'),
        ("setJarByClass", "Tells Hadoop which jar to ship to the task containers: the one containing this class."),
        ("setMapperClass", "Register the mapper and the reducer. There is no combiner: the mapper already reduces each split to one row."),
        ("setNumReduceTasks(1)", "Exactly one reducer, so one group, one answer and one output file."),
        ("setOutputKeyClass", "Output types. Map output uses the same types (Text, Text), so they do not need to be set separately."),
        ("addInputPath", "<code>args[0]</code> is the input path and <code>args[1]</code> the output path, taken from the <code>hadoop jar</code> command line."),
        ("waitForCompletion(true)", "Submit and wait. <code>true</code> prints progress (map 0% reduce 0% …) and counters. Exit code 0 means success."),
    ]) + """
<div class="box say"><b>If asked "why not just sort everything?"</b>Sorting would send all 4 million records
through the shuffle to answer a one-line question. Keeping the maximum inside each mapper means only 7 records
cross the network.</div>
"""


def s_mr2():
    rows = [["Multi-ply", "13.61", "1407.50", "118,352", "400.43"], ["Raw", "1.00", "1225.00", "1,845,444", "345.67"],
            ["Single-ply", "1.00", "1296.00", "1,284,703", "405.47"], ["Straps", "75.00", "765.00", "117", "295.59"],
            ["Unlimited", "9.98", "1372.12", "281,656", "368.85"], ["Wraps", "25.00", "1200.00", "229,693", "513.71"]]
    return """
<h2><small>MapReduce job 2</small>Summarization: min, max, count and average per equipment</h2>
<p><b>Question:</b> for each equipment category, what are the minimum, maximum, count and average TotalKg?<br>
<b>Pattern:</b> numerical summarization with a custom <code>Writable</code> and a combiner.</p>
""" + table(["Equipment", "Min", "Max", "Count", "Average"], rows, num=(1, 2, 3, 4)) + """
<p>Wraps has the highest average (513.71 kg). Raw has by far the most entries. Min values of 1 kg are odd data
entries in the source; we only removed empty values, not strange ones.</p>
""" + svg(860, 210, "".join([
        box(10, 60, 170, 90, "bxw", ["one row", "Raw, total 500"]),
        arrow(180, 105, 215, 105),
        box(218, 50, 190, 110, "bxa", ["Mapper emits", "(Raw, {min 500,", "max 500, sum 500,", "count 1})"]),
        arrow(408, 105, 440, 105),
        box(443, 50, 180, 110, "bx", ["Combiner merges", "per key inside", "each map task"]),
        arrow(623, 105, 655, 105),
        box(658, 50, 195, 110, "bxg", ["Reducer merges all,", "then avg = sum / count", "Raw: 1,845,444 rows", "avg 345.67"]),
    ]), "Every row becomes a tiny summary. Summaries merge into bigger summaries. The average is computed only at the very end.", "mr2 flow") + """
<h3>The custom value type</h3>
""" + code_block("mr/summarization/src/pl/summarization/MinMaxCountAvgTuple.java", [
        ("implements Writable", "Hadoop must send this object from mappers to reducers, so it implements <code>Writable</code>: two methods that turn it into bytes and back."),
        ("private double min, max, sum;", "It stores <b>sum and count</b>, never the average. Averages cannot be merged correctly; sums and counts can."),
        ("public void merge", "Merging two summaries: keep the smaller min and the larger max, and add the sums and the counts. The order and grouping of merges does not change the result, which is what makes a combiner safe."),
        ("readFields(DataInput in)", "Deserialize: read the four fields back from bytes."),
        ("write(DataOutput out)", "Serialize: write the four fields. The order here must be exactly the same as in <code>readFields</code>."),
        ("String.format", "When the reducer prints the tuple, the average is finally calculated as <code>sum / count</code>, formatted to 2 decimals."),
    ]) + """
<h3>Mapper</h3>
""" + code_block("mr/summarization/src/pl/summarization/SummarizationMapper.java", [
        ("extends Mapper<LongWritable, Text, Text, MinMaxCountAvgTuple>", "Output is (equipment name, summary tuple)."),
        ("private final Text equipment = new Text();", "The key and value objects are created once and reused for every row. <code>context.write</code> serializes them immediately, so reuse is safe and saves millions of allocations."),
        ('split(",", -1)', "Same parsing and the same three skip rules as MR1."),
        ("equipment.set(f[3]);", "Key = equipment category, column 3."),
        ("tuple.setMin(total); tuple.setMax(total);", "A one-row summary: min = max = sum = this total, count = 1."),
        ("ctx.write(equipment, tuple);", "Emit one pair per valid row."),
    ]) + """
<h3>Combiner</h3>
""" + code_block("mr/summarization/src/pl/summarization/SummarizationCombiner.java", [
        ("extends Reducer<Text, MinMaxCountAvgTuple, Text, MinMaxCountAvgTuple>", "A combiner is written as a Reducer. Its input <b>and</b> output types are both (Text, Tuple), the map output types, because its output goes into the shuffle as if the mapper had written it."),
        ("if (acc == null)", "Copy the first value into a fresh object. Hadoop reuses the object behind the iterator, so we must copy rather than keep a reference."),
        ("else acc.merge(v);", "Merge every other value into it."),
        ("ctx.write(key, acc);", "Each map task now sends a few summaries per equipment type instead of hundreds of thousands of rows. (The combiner can run more than once, on each spill of map output, so it is not always exactly one.)"),
    ]) + """
<h3>Reducer</h3>
""" + code_block("mr/summarization/src/pl/summarization/SummarizationReducer.java", [
        ("extends Reducer<Text, MinMaxCountAvgTuple, Text, Text>", "Output value is <b>Text</b>, not the tuple. Because the output type differs from the map output type, this class could not be the combiner, which is why MR2 has a separate Combiner class."),
        ("else acc.merge(v);", "Same merging logic as the combiner, over the partial summaries from all 7 map tasks."),
        ("new Text(acc.toString())", "Write the final line, e.g. <code>Raw⇥min=1.00⇥max=1225.00⇥count=1845444⇥avg=345.67</code>."),
    ]) + """
<h3>Driver</h3>
""" + code_block("mr/summarization/src/pl/summarization/SummarizationDriver.java", [
        ("setCombinerClass(SummarizationCombiner.class)", "Register the combiner."),
        ("setMapOutputKeyClass", "Map output types differ from the final output types (Tuple vs Text), so they <b>must</b> be declared separately here."),
        ("setOutputValueClass(Text.class)", "Final output value is Text."),
    ]) + """
<div class="box say"><b>If asked "why not store the average?"</b>The average of averages is wrong when groups
have different sizes. Example: avg(100) from 1 row and avg(200) from 3 rows gives (100 + 200) / 2 = 150, but the
true average is (100 + 600) / 4 = 175. Sums and counts always add up correctly.</div>
"""


def s_mr3():
    return """
<h2><small>MapReduce job 3</small>Federation: entries per federation</h2>
<p><b>Question:</b> how many competition entries has each federation run?<br>
<b>Pattern:</b> counting (word count), with the reducer reused as the combiner. <b>Result:</b> 475 federations;
THSPA 535,620, USAPL 365,199, THSWPA 325,029, USPA 232,091, FPR 191,693 at the top.</p>
""" + svg(860, 190, "".join([
        box(10, 50, 150, 90, "bxw", ["rows", "…,USAPL,…", "…,THSPA,…"]),
        arrow(160, 95, 195, 95),
        box(198, 40, 170, 110, "bxa", ["Mapper", "(USAPL, 1)", "(THSPA, 1)", "(USAPL, 1)"], mono=True),
        arrow(368, 95, 400, 95),
        box(403, 40, 170, 110, "bx", ["Combiner = Reducer", "(USAPL, 2)", "(THSPA, 1)"], mono=True),
        arrow(573, 95, 605, 95),
        box(608, 40, 245, 110, "bxg", ["Reducer adds all", "(THSPA, 535620)", "(USAPL, 365199)"], mono=True),
    ]), "Word count, where the \"word\" is column 34, Federation.", "mr3 flow") + """
<h3>Mapper</h3>
""" + code_block("mr/federation/src/pl/federation/FederationMapper.java", [
        ("private static final LongWritable ONE", "One shared <code>LongWritable(1)</code> object for every row, instead of creating a new one each time."),
        ("f[34].isEmpty()", "Skip broken rows, the header, and rows with no federation (column 34)."),
        ("fed.set(f[34]);", "Key = federation name."),
        ("ctx.write(fed, ONE);", "Emit (federation, 1) for every entry."),
    ]) + """
<h3>Reducer (also the combiner)</h3>
""" + code_block("mr/federation/src/pl/federation/FederationReducer.java", [
        ("extends Reducer<Text, LongWritable, Text, LongWritable>", "Input and output types are identical: (Text, LongWritable). That is the condition that lets this class also be the combiner."),
        ("for (LongWritable v : values) sum += v.get();", "Add up the values. As a combiner the values are 1s; in the final reducer they are partial counts. Addition gives the same answer either way."),
        ("ctx.write(key, new LongWritable(sum));", "Write (federation, count)."),
    ]) + """
<h3>Driver</h3>
""" + code_block("mr/federation/src/pl/federation/FederationDriver.java", [
        ("setCombinerClass(FederationReducer.class)", "The same class registered twice: once as combiner, once as reducer."),
        ("setOutputValueClass(LongWritable.class)", "Map and final output types are the same, so only the output classes are set."),
    ]) + """
<div class="box warn"><b>Output order</b>MR3's <code>part-r-00000</code> is sorted <b>alphabetically by federation</b>,
because the shuffle sorts by key. To rank by count we sort afterwards in the terminal:
<code>hdfs dfs -cat /powerlifting/out_federation/part-r-00000 | sort -t$'\\t' -k2 -nr | head -10</code>.</div>
"""


def s_pigtheory():
    return """
<h2><small>Theory 3</small>Apache Pig</h2>
<p><b>Pig</b> is a high-level platform on top of Hadoop. You write a script in <b>Pig Latin</b>, a dataflow
language where each line transforms a dataset, and Pig compiles the script into MapReduce jobs for you.</p>
""" + svg(860, 150, "".join([
        box(10, 40, 150, 70, "bxv", ["Pig Latin script", ".pig file"]),
        arrow(160, 75, 195, 75),
        box(198, 40, 140, 70, "bx", ["Logical plan", "parse + check"]),
        arrow(338, 75, 373, 75),
        box(376, 40, 140, 70, "bx", ["Physical plan", "operators"]),
        arrow(516, 75, 551, 75),
        box(554, 40, 140, 70, "bxa", ["MapReduce plan", "1 or more jobs"]),
        arrow(694, 75, 729, 75),
        box(732, 40, 120, 70, "bxg", ["YARN", "runs them"]),
    ]), "What happens when you run <code>pig -x mapreduce -f script.pig</code>.", "pig compile") + table(["Term", "Meaning"], [
        ["Relation", "a named dataset, like <code>raw</code> or <code>clean</code>. Each statement creates a new relation."],
        ["Tuple", "one record: an ordered list of fields, like a row"],
        ["Bag", "a collection of tuples. After <code>GROUP</code>, each group holds a bag of its rows."],
        ["Field", "one value in a tuple. Without a schema, fields are named by position: <code>$0</code>, <code>$1</code>, …"],
        ["Schema", "field names and types. Declared with <code>AS (name:type, …)</code> or by casting in <code>FOREACH</code>."],
        ["Lazy evaluation", "nothing runs while statements are defined. Only <code>STORE</code> or <code>DUMP</code> triggers execution."],
    ]) + """
<h3>Execution modes</h3>
""" + table(["Mode", "Command", "Reads and writes"], [
        ["Local", "<code>pig -x local -f script.pig</code>", "the local filesystem, single JVM, good for testing"],
        ["MapReduce (what we used)", "<code>pig -x mapreduce -f script.pig</code>", "HDFS; runs real MapReduce jobs on YARN"],
        ["Interactive (Grunt shell)", "<code>pig</code> (then type statements)", "same as the chosen mode; <code>quit;</code> to leave"],
    ]) + """
<h3>Operators we used</h3>
""" + table(["Operator", "What it does", "Our use"], [
        ["<code>LOAD … USING PigStorage(',')</code>", "reads a file, splitting each line on the delimiter", "read the CSV from HDFS, no schema"],
        ["<code>FILTER … BY</code>", "keeps tuples where the condition is true", "drop the header and empty values"],
        ["<code>FOREACH … GENERATE</code>", "projects and transforms fields, one output tuple per input tuple", "pick 2–3 columns and cast types"],
        ["<code>GROUP … BY x</code> / <code>GROUP … ALL</code>", "collects tuples with the same key into a bag / everything into one bag", "per-category vs global results"],
        ["<code>COUNT(bag)</code>", "number of tuples in a bag", "entries per federation"],
        ["<code>ORDER … BY x DESC</code>", "sorts", "highest first, nested inside FOREACH"],
        ["<code>LIMIT n</code>", "keeps the first n tuples", "top 5 or top 10"],
        ["<code>FLATTEN(bag)</code>", "un-nests a bag into separate tuples", "turn the top-10 bag back into 10 rows"],
        ["<code>STORE … INTO</code>", "writes the relation to HDFS and triggers the run", "write the result directory"],
    ]) + """
<h3>Handy Grunt shell commands</h3>
<ul>
<li><code>DUMP rel;</code> runs the script up to <code>rel</code> and prints the result on screen.</li>
<li><code>DESCRIBE rel;</code> prints the schema of a relation.</li>
<li><code>EXPLAIN rel;</code> prints the logical, physical and MapReduce plans.</li>
<li><code>ILLUSTRATE rel;</code> shows a small sample of data flowing through each step.</li>
</ul>
<div class="box say"><b>MapReduce vs Pig in one sentence</b>MapReduce gives full control (we chose the combiner and wrote a custom
Writable) but needs a lot of Java. Pig needs about ten lines per question and writes the map and reduce steps
itself, at the cost of some control.</div>
"""


def s_pig():
    return """
<h2><small>Pig scripts</small>The five Pig analyses</h2>
<p>All five scripts share the same first three lines, then differ only in grouping and sorting. Learn one and you know all five.</p>
<h3>Pig 1: top 5 federations (cross-checks MR3)</h3>
""" + code_block("pig/top5Federations.pig", [
        ("LOAD '/powerlifting/openpowerlifting.csv' USING PigStorage(',')", "Read the CSV from HDFS, splitting on commas. No schema is given, so fields are <code>$0 … $41</code> of unknown type (bytearray)."),
        ("FILTER raw BY $0 != 'Name' AND $34 != ''", "Drop the header row (its first field is the text <code>Name</code>) and rows with an empty Federation."),
        ("GENERATE (chararray)$34 AS federation", "Keep only column 34, cast to text and named <code>federation</code>. Throwing away the other 41 columns early makes everything after this cheaper."),
        ("GROUP feds BY federation", "One group per federation. Each group is (group = name, bag of that federation's tuples)."),
        ("COUNT(feds) AS cnt", "Count the tuples in each bag. <code>group</code> is the grouping key."),
        ("GROUP counts ALL", "Put all 475 (federation, count) tuples into a single bag so they can be ranked together."),
        ("ORDER counts BY cnt DESC", "Nested block: inside the single group, sort by count, highest first…"),
        ("LIMIT sorted 5", "…keep the first 5…"),
        ("GENERATE FLATTEN(lim)", "…and flatten the bag into 5 ordinary rows."),
        ("STORE top5 INTO 'Top5Federations.txt'", "Write the result. A relative path goes to the HDFS home directory: <code>/user/shinzuu/Top5Federations.txt/part-r-00000</code>. This line starts the actual execution."),
    ]) + """
<p>Output: THSPA 535620, USAPL 365199, THSWPA 325029, USPA 232091, FPR 191693. <b>Exactly the same as MR3's top
5</b>, computed by a different engine. This script groups twice, so Pig compiled it into <b>2 MapReduce jobs</b>;
that is why the YARN UI shows 9 applications for our 8 analyses.</p>
<h3>Pig 2: top 10 totals of all time</h3>
""" + code_block("pig/top10Total.pig", [
        ("$25 != ''", "Keep only rows with a TotalKg (column 25)."),
        ("(chararray)$0 AS name, (chararray)$3 AS equipment, (double)$25 AS total", "Keep name, equipment and total. Casting total to <code>double</code> is essential: sorted as text, \"999\" would come before \"1000\"."),
        ("GROUP lifts ALL", "<code>ALL</code> puts every row into one group, so the ranking is global."),
        ("ORDER lifts BY total DESC", "Sort all rows by total, highest first, inside the nested block."),
        ("LIMIT sorted 10", "Keep 10."),
        ("STORE top10 INTO 'Top10Total.txt'", "Write to <code>/user/shinzuu/Top10Total.txt</code>."),
    ]) + table(["#", "Name", "Equipment", "Total (kg)"], [
        ["1", "Dave Hoff #1", "Multi-ply", "1407.5"], ["2", "Dave Hoff #1", "Multi-ply", "1387.5"], ["3", "Rodney Woodward", "Unlimited", "1372.12"],
        ["4", "Dave Hoff #1", "Multi-ply", "1370.0"], ["5", "Dave Hoff #1", "Multi-ply", "1367.5"], ["6", "Dave Hoff #1", "Multi-ply", "1365.31"],
        ["7", "Dave Hoff #1", "Multi-ply", "1363.05"], ["8", "Donnie Thompson #1", "Multi-ply", "1360.78"], ["9", "Dave Hoff #1", "Multi-ply", "1350.0"],
        ["10", "Dave Hoff #1", "Multi-ply", "1345.0"]], num=(0, 3)) + """
<p>Dave Hoff holds 8 of the top 10. The same lifter appears many times because each row is one competition.</p>
<h3>Pig 3: top 10 totals within each equipment category</h3>
""" + code_block("pig/top10TotalByEquipment.pig", [
        ("GROUP lifts BY equipment", "The only real change from Pig 2: <code>BY equipment</code> instead of <code>ALL</code>. Now there are 6 groups."),
        ("ORDER lifts BY total DESC", "The nested sort and limit now run <b>inside each group</b> separately."),
        ("GENERATE FLATTEN(lim)", "10 rows per category, 60 rows in total."),
    ]) + table(["Equipment", "Best total", "Lifter"], [
        ["Multi-ply", "1407.5", "Dave Hoff #1"], ["Unlimited", "1372.12", "Rodney Woodward"], ["Single-ply", "1296.0", "Blaine Sumner"],
        ["Raw", "1225.0", "Colton Engelbrecht"], ["Wraps", "1200.0", "Colton Engelbrecht"], ["Straps", "765.0", "William Crozier"]], num=(1,)) + """
<div class="box deep"><b>Why this script is the best argument for Pig</b>Top 10 <i>per category</i> in raw MapReduce
needs a secondary sort: a custom composite key, partitioner, sort comparator and grouping comparator. In Pig it is a
one-word change from <code>ALL</code> to <code>BY equipment</code>.</div>
<h3>Pig 4: top 10 Dots scores</h3>
""" + code_block("pig/top10Dots.pig", [
        ("$27 != ''", "Keep only rows with a Dots score (column 27)."),
        ("(chararray)$1 AS sex, (double)$27 AS dots", "Keep name, sex and Dots, with Dots cast to a number."),
        ("GROUP lifts ALL", "Global ranking, as in Pig 2."),
        ("ORDER lifts BY dots DESC", "Sort by Dots, highest first, and keep 10."),
    ]) + table(["#", "Name", "Sex", "Dots"], [
        ["1", "Deana Tollefson", "F", "818.06"], ["2", "Jenna Odziana", "F", "808.17"], ["3", "Taylor Schaeffer", "F", "802.47"],
        ["4", "Deana Tollefson", "F", "799.11"], ["5", "Laura Phelps-Stackhouse", "F", "795.22"], ["6", "Taylor Schaeffer", "F", "789.33"],
        ["7", "Deana Tollefson", "F", "788.67"], ["8", "Deana Tollefson", "F", "787.9"], ["9", "Deana Tollefson", "F", "783.79"],
        ["10", "Dave Hoff #1", "M", "783.48"]], num=(0, 3)) + """
<p>9 of the top 10 are women and Deana Tollefson holds 5 places. Dots adjusts for bodyweight, so lighter lifters
who lift a lot relative to their size score highest.</p>
<h3>Pig 5: top 10 Dots within each sex category</h3>
""" + code_block("pig/top10DotsBySex.pig", [
        ("GROUP lifts BY sex", "Same as Pig 4 but grouped by sex: 3 groups (F, M, Mx), 10 rows each, 30 rows in total."),
        ("ORDER lifts BY dots DESC", "Sort and limit inside each sex group."),
    ]) + table(["Sex", "Best Dots", "Lifter"], [["F", "818.06", "Deana Tollefson"], ["M", "783.48", "Dave Hoff #1"], ["Mx", "407.79", "Emilio Valle"]], num=(1,)) + """
<div class="box warn"><b>Why every sort is nested</b>With Pig 0.17 on Hadoop 3 a top-level <code>ORDER BY</code>
failed for us, so every sort lives inside <code>FOREACH (GROUP …) { ORDER …; LIMIT …; }</code>. For top-N
questions that is the natural way to write it anyway.</div>
"""


def s_compare():
    return """
<h2><small>Compare</small>MapReduce vs Pig, and how we verified</h2>
""" + table(["", "Java MapReduce", "Pig Latin"], [
        ["Code size", "3 to 5 Java classes per job", "about 10 lines per script"],
        ["Level", "low level: you write map and reduce", "high level: you describe the dataflow"],
        ["Control", "full: combiner, custom Writable, number of reducers", "Pig decides the plan"],
        ["Grouped top-N", "needs secondary sort (several extra classes)", "change <code>ALL</code> to <code>BY x</code>"],
        ["Compile step", "<code>javac</code> + <code>jar</code>", "none, Pig compiles the script at run time"],
        ["Run command", "<code>hadoop jar X.jar MainClass in out</code>", "<code>pig -x mapreduce -f X.pig</code>"],
        ["Output path", "given on the command line", "set by <code>STORE … INTO</code>"],
        ["Our run time", "about 35–40 s per job", "about 1 minute per script"],
        ["Engine underneath", "MapReduce on YARN", "also MapReduce on YARN"],
    ]) + """
<h3>How we know the numbers are right</h3>
<ol class="steps">
<li><b>Independent recompute</b><code>scripts/groundtruth.sh</code> answers all eight questions with awk directly over the local CSV. No HDFS, no Java, no shuffle, so a bug in our Hadoop code cannot also be in this path.</li>
<li><b>Compare</b><code>scripts/sync_report_numbers.py</code> compares cluster outputs with the awk answers (counts exactly, decimals to 2 places) and refuses to update the report if any value disagrees.</li>
<li><b>Cross-check engines</b>MR3 (Java) and Pig 1 answer the same question. Their top 5 are identical.</li>
<li><b>Live check in the demo</b>After each job we pipe the HDFS output into <code>diff</code> against the saved result file and print <code>MATCHES REPORT</code>. On the full run, 8 out of 8 matched.</li>
</ol>
"""


def s_terminal():
    return """
<h2><small>Terminal</small>Commands you may be asked to type</h2>
<p>The section that took the exam before us was asked to type commands in the terminal and show how to run
things. Practise these until you can type them without looking.</p>
<h3>1. Start the cluster and check it</h3>
""" + shell([
        ("start-dfs.sh", "starts NameNode, DataNode, SecondaryNameNode"),
        ("start-yarn.sh", "starts ResourceManager, NodeManager"),
        ("mapred --daemon start historyserver", "starts JobHistoryServer"),
        ("hdfs dfsadmin -safemode wait", "wait until HDFS allows writes"),
        ("jps", "list the Java processes: expect all 6"),
        ("hdfs dfsadmin -report", "capacity, live DataNodes, used space"),
    ]) + """
<h3>2. HDFS file commands</h3>
""" + shell([
        ("hdfs dfs -mkdir -p /powerlifting", "make a directory (-p: parents too)"),
        ("hdfs dfs -put data/openpowerlifting-2026-09-05/openpowerlifting-2026-09-05-b8b9bf6e.csv /powerlifting/openpowerlifting.csv", "upload local file to HDFS"),
        ("hdfs dfs -ls /", "list the HDFS root"),
        ("hdfs dfs -ls -h /powerlifting", "list with human-readable sizes"),
        ("hdfs dfs -du -h /powerlifting", "space used"),
        ("hdfs dfs -head /powerlifting/openpowerlifting.csv", "first kilobyte of a file"),
        ("hdfs dfs -cat /powerlifting/out_toptotal/part-r-00000", "print a file"),
        ("hdfs dfs -get /powerlifting/out_toptotal/part-r-00000 mr1.txt", "download from HDFS to local"),
        ("hdfs dfs -rm -r -f /powerlifting/out_toptotal", "delete a directory (-r recursive, -f no error if missing)"),
        ("hdfs fsck /powerlifting/openpowerlifting.csv -files -blocks", "show the file's blocks (7 of them)"),
    ]) + """
<h3>3. Compile and run a MapReduce job (MR1 as the example)</h3>
""" + shell([
        ("cd ~/Documents/study/bdal-powerlifting-analysis/mr/toptotal", ""),
        ('javac -cp "$(hadoop classpath)" -d build src/pl/toptotal/*.java', "compile against the Hadoop jars"),
        ("jar cf TopTotal.jar -C build .", "pack the .class files into a jar"),
        ("jar tf TopTotal.jar", "list what is inside the jar"),
        ("hadoop jar TopTotal.jar pl.toptotal.TopTotalDriver /powerlifting/openpowerlifting.csv /powerlifting/out_toptotal", "jar, main class, input, output"),
        ("hdfs dfs -ls /powerlifting/out_toptotal", "_SUCCESS and part-r-00000"),
        ("hdfs dfs -cat /powerlifting/out_toptotal/part-r-00000", "the answer"),
    ]) + """
<p>MR2 and MR3 are the same with a different folder, jar and main class:</p>
""" + shell([
        ("hadoop jar Summarization.jar pl.summarization.SummarizationDriver /powerlifting/openpowerlifting.csv /powerlifting/out_summarization", ""),
        ("hadoop jar Federation.jar pl.federation.FederationDriver /powerlifting/openpowerlifting.csv /powerlifting/out_federation", ""),
        ("hdfs dfs -cat /powerlifting/out_federation/part-r-00000 | sort -t$'\\t' -k2 -nr | head -10", "rank federations by count"),
    ]) + """
<h3>4. Run a Pig script</h3>
""" + shell([
        ("cd ~/Documents/study/bdal-powerlifting-analysis/pig", ""),
        ("cat top10Dots.pig", "show the script first"),
        ("pig -x mapreduce -f top10Dots.pig", "run on the cluster"),
        ("hdfs dfs -ls", "no path = HDFS home, /user/shinzuu"),
        ("hdfs dfs -cat 'Top10Dots.txt/part-*'", "quote the glob"),
    ]) + """
<h3>5. Watch jobs, then stop</h3>
""" + shell([
        ("yarn application -list", "running applications"),
        ("yarn application -list -appStates FINISHED", "finished applications"),
        ("yarn application -kill application_<id>", "stop a stuck job"),
        ("mapred --daemon stop historyserver", ""),
        ("stop-yarn.sh", ""),
        ("stop-dfs.sh", ""),
    ]) + """
<h3>6. Look at the dataset without Hadoop</h3>
""" + shell([
        ("head -1 openpowerlifting-2026-09-05-b8b9bf6e.csv | tr ',' '\\n' | cat -n", "column list, numbered from 1"),
        ("head -5 openpowerlifting-2026-09-05-b8b9bf6e.csv", "first rows"),
        ("wc -l openpowerlifting-2026-09-05-b8b9bf6e.csv", "4030220 lines = rows + header"),
        ("du -h openpowerlifting-2026-09-05-b8b9bf6e.csv", "786M on local disk"),
        ("awk -F, 'NF!=42{c++} END{print c+0}' openpowerlifting-2026-09-05-b8b9bf6e.csv", "0 = every row has 42 fields"),
    ]) + """
<h3>Errors you might see live</h3>
""" + table(["Message", "Meaning", "Fix"], [
        ["<code>FileAlreadyExistsException: Output directory … already exists</code>", "output path left from an earlier run", "<code>hdfs dfs -rm -r -f &lt;out&gt;</code>, run again"],
        ["<code>SafeModeException: Name node is in safe mode</code>", "HDFS still starting up", "<code>hdfs dfsadmin -safemode wait</code>"],
        ["job stuck at <code>map 0% reduce 0%</code>", "no NodeManager running", "<code>jps</code>; if missing, <code>start-yarn.sh</code>"],
        ["<code>ClassNotFoundException: pl.toptotal.TopTotalDriver</code>", "wrong class name or jar", "use the full package name; <code>jar tf</code> to check"],
        ["<code>Connection refused … localhost:9000</code>", "HDFS is not running", "<code>start-dfs.sh</code>"],
        ["<code>No such file or directory</code> with <code>part-*</code>", "local shell expanded the glob", "put the HDFS path in single quotes"],
    ]) + """
<h3>Drill: hide the answer, type it, then check</h3>
<div class="drill" id="drill"></div>
"""


def out(lines):
    """Terminal output block (no prompt)."""
    import html as _h
    rows = "".join(f"<span>{_h.escape(l)}</span>" for l in lines)
    return f'<pre class="term"><code>{rows}</code></pre>'


def s_lab2():
    return """
<h2><small>Lab 2</small>Basic HDFS commands (the one the examiner is asking for)</h2>
<p>Students in the other section were asked to run the <b>Lab 2</b> commands live: Experiment 01, "Installation
Verification and Basic Hadoop HDFS Commands". Every command and output below was run on this laptop's cluster.
The sample files <code>command3.txt</code> and <code>exampleput.txt</code> are in
<code>~/Documents/study/hadoop-bdal-lab-kit/Lab-2-HDFS-Basic-Commands</code>.</p>
<div class="box deep"><b>The key idea</b>HDFS is a <b>separate filesystem</b> from your normal disk. A file in your
home folder is not in HDFS. You reach HDFS only through <code>hadoop fs -…</code> or <code>hdfs dfs -…</code>
(they are the same for HDFS). A path starting with <code>/</code> is from the HDFS root; a path with no
<code>/</code> is relative to your HDFS home, <code>/user/shinzuu</code>.</div>
<h3>Step by step, with real output</h3>
<h4>1. Start Hadoop and verify the services</h4>
""" + shell([("cd ~/Documents/study/hadoop-bdal-lab-kit/Lab-2-HDFS-Basic-Commands", "the folder with the sample files"),
             ("hadoop-start", "our alias: start-dfs.sh + start-yarn.sh + history server + jps"),
             ("jps", "")]) + out(["NameNode", "DataNode", "SecondaryNameNode", "ResourceManager", "NodeManager", "JobHistoryServer", "Jps"]) + """
<p>The Windows lab sheet uses <code>start-all.cmd</code> and lists 4 services. On Linux we start HDFS and YARN
separately, and our setup also shows SecondaryNameNode and JobHistoryServer.</p>
<h4>2. List the HDFS root</h4>
""" + shell([("hadoop fs -ls /", "")]) + out(["Found 3 items",
    "drwxr-xr-x   - shinzuu supergroup          0 2026-09-15 14:22 /powerlifting",
    "drwxrwx---   - shinzuu supergroup          0 2026-09-15 13:47 /tmp",
    "drwxr-xr-x   - shinzuu supergroup          0 2026-09-11 21:42 /user"]) + """
<h4>3. Create a directory and a subdirectory</h4>
""" + shell([("hadoop fs -mkdir /dir1", ""), ("hadoop fs -ls /", "/dir1 now appears"),
             ("hadoop fs -mkdir /dir1/newdir", ""), ("hadoop fs -ls /dir1", "")]) + out(["Found 1 items",
    "drwxr-xr-x   - shinzuu supergroup          0 2026-09-15 23:03 /dir1/newdir"]) + """
<h4>4. Copy a local file into HDFS (copyFromLocal)</h4>
""" + shell([("hadoop fs -copyFromLocal command3.txt /dir1", ""), ("hadoop fs -ls /dir1", "")]) + out(["Found 2 items",
    "-rw-r--r--   1 shinzuu supergroup         38 2026-09-15 23:03 /dir1/command3.txt",
    "drwxr-xr-x   - shinzuu supergroup          0 2026-09-15 23:03 /dir1/newdir"]) + """
<p>Read the listing: <code>-rw-r--r--</code> is a file (<code>d</code> would be a directory), <code>1</code> is the
replication factor, <code>38</code> is the size in bytes. Directories show <code>-</code> for replication.</p>
<h4>5. Copy a file out of HDFS (copyToLocal)</h4>
""" + shell([("mkdir -p downloaded", "a normal local folder"), ("hadoop fs -copyToLocal /dir1/command3.txt downloaded/", "")]) + """
<h4>6. The same with put and get</h4>
""" + shell([("hadoop fs -put exampleput.txt /dir1/newdir", "put = copyFromLocal"),
             ("hadoop fs -get /dir1/newdir/exampleput.txt downloaded/", "get = copyToLocal"),
             ("ls downloaded", "")]) + out(["command3.txt", "exampleput.txt"]) + """
<h4>7. Show a file's contents</h4>
""" + shell([("hadoop fs -cat /dir1/command3.txt", "")]) + out(["command3 - hello from HDFS basics lab"]) + """
<h4>8. Delete a file</h4>
""" + shell([("hadoop fs -rm /dir1/command3.txt", "")]) + out(["Deleted /dir1/command3.txt"]) + """
<h4>9. Delete an empty directory (rmdir)</h4>
""" + shell([("hadoop fs -rm /dir1/newdir/exampleput.txt", "empty it first"), ("hadoop fs -rmdir /dir1/newdir", "")]) + """
<h4>10. Delete a non-empty directory (rm -r)</h4>
""" + shell([("hadoop fs -rm -r /dir1", "")]) + out(["Deleted /dir1"]) + """
<h4>11. Check the final state and the web UI</h4>
""" + shell([("hadoop fs -ls /", "back to /powerlifting, /tmp, /user")]) + """
<p>Then open <b>http://localhost:9870 → Utilities → Browse the file system</b>. It shows the same HDFS as
<code>hadoop fs -ls</code>.</p>
<h3>Errors you can trigger, and what they mean</h3>
<p>These are real messages from this cluster. Knowing them shows you understand the commands, not just memorised them.</p>
""" + table(["You type", "HDFS replies", "Why"], [
        ["<code>hadoop fs -rmdir /dir1/newdir</code> (with a file inside)", "<code>rmdir: `/dir1/newdir': Directory is not empty</code>", "<code>-rmdir</code> only removes empty directories"],
        ["<code>hadoop fs -rm /dir1</code>", "<code>rm: `/dir1': Is a directory</code>", "a directory needs <code>-rm -r</code>"],
        ["<code>hadoop fs -copyFromLocal command3.txt /dir1</code> twice", "<code>copyFromLocal: `/dir1/command3.txt': File exists</code>", "HDFS does not overwrite; use <code>-put -f</code>"],
        ["<code>hadoop fs -mkdir /dir1/x/y</code> when /dir1/x does not exist", "<code>mkdir: `hdfs://localhost:9000/dir1/x': No such file or directory</code>", "parents are not created; use <code>-mkdir -p</code>"],
        ["<code>hadoop fs -cat /dir1/missing.txt</code>", "<code>cat: `/dir1/missing.txt': No such file or directory</code>", "wrong path, or the file is local, not in HDFS"],
    ]) + """
<h3>More HDFS commands worth knowing (all tested)</h3>
""" + table(["Task", "Command", "Real output / note"], [
        ["make parent dirs too", "<code>hadoop fs -mkdir -p /dir1/newdir</code>", "no error if it already exists"],
        ["overwrite on upload", "<code>hadoop fs -put -f command3.txt /dir1</code>", "replaces the existing file"],
        ["create an empty file", "<code>hadoop fs -touchz /dir1/empty.txt</code>", "0-byte file"],
        ["copy inside HDFS", "<code>hadoop fs -cp /dir1/command3.txt /dir1/newdir/copy.txt</code>", ""],
        ["move / rename inside HDFS", "<code>hadoop fs -mv /dir1/empty.txt /dir1/newdir/</code>", ""],
        ["list recursively", "<code>hadoop fs -ls -R /dir1</code>", "every file and subfolder"],
        ["size of each item", "<code>hadoop fs -du -h /dir1</code>", "<code>38  38  /dir1/command3.txt</code>"],
        ["total size", "<code>hadoop fs -du -s -h /dir1</code>", "<code>76  76  /dir1</code>"],
        ["count dirs, files, bytes", "<code>hadoop fs -count /dir1</code>", "<code>2  3  76 /dir1</code>"],
        ["last kilobyte of a file", "<code>hadoop fs -tail /dir1/command3.txt</code>", ""],
        ["file details", "<code>hadoop fs -stat \"%n %b bytes %r replicas\" /dir1/command3.txt</code>", "<code>command3.txt 38 bytes 1 replicas</code>"],
        ["append a local file", "<code>hadoop fs -appendToFile exampleput.txt /dir1/command3.txt</code>", "cat now shows both lines"],
        ["change permissions", "<code>hadoop fs -chmod 755 /dir1/command3.txt</code>", ""],
        ["show a file's blocks", "<code>hdfs fsck /powerlifting/openpowerlifting.csv -files -blocks</code>", "<code>823619397 bytes, replication=1, 7 block(s): OK</code>"],
        ["cluster report", "<code>hdfs dfsadmin -report</code>", "capacity, used space, live DataNodes"],
        ["YARN nodes", "<code>yarn node -list</code>", "<code>Total Nodes:1</code>, state RUNNING"],
    ]) + """
<h3>Show your own project data with Lab 2 commands</h3>
""" + shell([("hadoop fs -ls -h /powerlifting", ""), ("hadoop fs -du -h /powerlifting", "")]) + out(["785.5 M  785.5 M  /powerlifting/openpowerlifting.csv"]) + shell([("hdfs fsck /powerlifting/openpowerlifting.csv -files -blocks", "")]) + out([
        "/powerlifting/openpowerlifting.csv 823619397 bytes, replicated: replication=1, 7 block(s):  OK",
        "0. BP-…:blk_1073741825_1001 len=134217728 Live_repl=1",
        "…",
        "6. BP-…:blk_1073741831_1007 len=18313029 Live_repl=1",
        "Status: HEALTHY"]) + """
<p>Six full blocks of 134,217,728 bytes (128 MB) plus a last block of 18,313,029 bytes. That is exactly why every
job on this page ran <b>7 map tasks</b>.</p>
<div class="box warn"><b>Two gotchas from Lab 2</b>A local folder name with a space (like <code>Lab 2</code>) breaks
Hadoop's local path handling, so <code>cd</code> into the folder and pass just the filename. And the
<code>WARN util.NativeCodeLoader</code> line printed by every command is harmless: Hadoop is using its Java
libraries instead of optional native ones.</div>
"""


QA = [
    # lab 2
    ("lab 2", "What is the difference between hadoop fs and hdfs dfs?", "For HDFS they do the same thing. hadoop fs is the generic filesystem shell that can work with any Hadoop filesystem; hdfs dfs is specific to HDFS."),
    ("lab 2", "What is the difference between put and copyFromLocal?", "Both copy a local file into HDFS. copyFromLocal only accepts a local source; put can also read from standard input. For the lab they behave the same."),
    ("lab 2", "What is the difference between get and copyToLocal?", "Both copy a file from HDFS to the local disk; copyToLocal is restricted to a local destination. In practice they are the same."),
    ("lab 2", "rmdir vs rm -r?", "hadoop fs -rmdir removes only an empty directory and fails with \"Directory is not empty\" otherwise. hadoop fs -rm -r deletes a directory and everything inside it."),
    ("lab 2", "How do you create nested directories in one command?", "hadoop fs -mkdir -p /dir1/x/y. Without -p it fails with \"No such file or directory\" when a parent is missing."),
    ("lab 2", "How do you overwrite a file that already exists in HDFS?", "hadoop fs -put -f localfile /path. Without -f, copyFromLocal and put fail with \"File exists\"."),
    ("lab 2", "In hadoop fs -ls output, what is the number after the permissions?", "The replication factor of the file (1 on our cluster). Directories show a dash because they have no blocks."),
    ("lab 2", "How can you see how a file is stored in blocks?", "hdfs fsck <path> -files -blocks. For our CSV it shows 823619397 bytes, replication=1, 7 blocks: six of 134217728 bytes and one of 18313029."),
    ("lab 2", "Where does hadoop fs -ls with no path look?", "In your HDFS home directory, /user/<username>, which is /user/shinzuu here."),
    ("lab 2", "How do you check HDFS from a browser?", "NameNode web UI at http://localhost:9870, then Utilities → Browse the file system."),
    ("lab 2", "What does the NativeCodeLoader warning mean?", "Hadoop could not load its optional native (C) libraries and is using the built-in Java versions. It is harmless."),
    # dataset
    ("dataset", "What dataset did you use and where is it from?", "The OpenPowerlifting archive, a volunteer-maintained record of powerlifting competition results worldwide, downloaded as one bulk CSV from openpowerlifting.org. Snapshot dated 2026-09-05."),
    ("dataset", "How big is it?", "785.5 MB (823,619,397 bytes), 4,030,219 data rows plus a header, 42 columns. About 170 MB as a zip."),
    ("dataset", "What does one row represent?", "One lifter's result at one competition. A lifter who competed many times has many rows."),
    ("dataset", "Is it legal to use?", "Yes. The data is public domain: OpenPowerlifting waives copyright and only asks for attribution."),
    ("dataset", "Which columns did you use, and at which indexes?", "Name $0, Sex $1, Equipment $3, TotalKg $25, Dots $27, Federation $34, Date $36. Indexes are 0-based."),
    ("dataset", "What is TotalKg?", "The sum of a lifter's best successful squat, bench press and deadlift, in kilograms."),
    ("dataset", "What is Dots and why does it exist?", "A bodyweight-adjusted score: total × 500 divided by a 4th-degree polynomial of bodyweight, with separate coefficients for men and women. It lets lifters of different sizes be compared, which is why its top 10 is mostly women."),
    ("dataset", "How did you handle missing or bad values?", "Rows with an empty value in the column a job needs are skipped (270,254 empty TotalKg, 296,478 empty Dots). The header row is skipped, and in Java a non-numeric value is caught and skipped. We did not remove unusual but valid-looking values like a 1 kg total."),
    ("dataset", "Did you need a CSV parser for quoted fields?", "No. We checked with awk that every row has exactly 42 comma-separated fields and no field contains a quote, so a plain split on commas is correct."),
    ("dataset", "Why are Texas high-school federations on top?", "THSPA and THSWPA run very frequent, large high-school meets and record every entry, so by entry count they beat every national federation."),
    ("dataset", "What are the equipment categories?", "Raw, Wraps, Single-ply, Multi-ply, Unlimited and Straps. Raw is the largest; Multi-ply holds the all-time total record."),
    # hadoop
    ("hadoop", "What is Hadoop?", "An open-source framework for storing and processing very large datasets across a cluster of ordinary machines. Its core is HDFS for storage and YARN for running jobs, with MapReduce as the processing model."),
    ("hadoop", "What mode did you run Hadoop in?", "Pseudo-distributed: all six daemons run on one machine as separate Java processes, talking over localhost."),
    ("hadoop", "Name the six daemons and what each does.", "NameNode (HDFS metadata), DataNode (stores blocks), SecondaryNameNode (checkpoints metadata), ResourceManager (schedules the cluster's resources), NodeManager (runs task containers on a node), JobHistoryServer (keeps finished-job history)."),
    ("hadoop", "What is a block, and how many does your file have?", "HDFS stores files as fixed-size blocks, 128 MB by default. Our 785.5 MB file has 7 blocks, which is why each job has 7 map tasks."),
    ("hadoop", "What is the replication factor and why is yours 1?", "The number of copies of each block, normally 3. We have one DataNode, so only one copy is possible; we set dfs.replication to 1."),
    ("hadoop", "Is the SecondaryNameNode a backup?", "No. It merges the edit log into the fsimage (checkpointing). It cannot take over if the NameNode fails."),
    ("hadoop", "What does the NameNode store?", "Only metadata: the directory tree, file-to-block mapping and block locations. The data itself is on DataNodes."),
    ("hadoop", "What is safe mode?", "A read-only state at NameNode startup while it waits for DataNodes to report their blocks. Writes and jobs fail until it ends; hdfs dfsadmin -safemode wait blocks until then."),
    ("hadoop", "Why does Hadoop need SSH on a single machine?", "The start scripts (start-dfs.sh, start-yarn.sh) launch each daemon over SSH, even when the host is localhost, so passwordless SSH is required."),
    ("hadoop", "What is in your four config files?", "core-site: fs.defaultFS hdfs://localhost:9000. hdfs-site: replication 1, NameNode and DataNode directories, SecondaryNameNode on localhost:9868. mapred-site: mapreduce.framework.name = yarn. yarn-site: aux-services = mapreduce_shuffle."),
    ("hadoop", "What are the YARN components?", "ResourceManager (one per cluster), NodeManager (one per node), a per-job ApplicationMaster, and containers where tasks run."),
    ("hadoop", "Which Java version and why?", "OpenJDK 11. Hadoop 3.4.x supports Java 8 and 11 at runtime; newer versions do not work."),
    ("hadoop", "Why do you format the NameNode only once?", "Formatting creates a new, empty filesystem. Doing it again wipes all metadata, so the data already in HDFS is lost."),
    # mapreduce theory
    ("mapreduce", "Explain MapReduce in simple terms.", "Map processes each input record independently and emits key-value pairs. Hadoop shuffles and sorts them so all values for one key are together. Reduce then processes each key's list of values to produce the result."),
    ("mapreduce", "What is the shuffle?", "The phase that copies map output to reducers, partitions it by key, sorts it and groups values with the same key. It moves data over the network, so it is usually the most expensive step."),
    ("mapreduce", "What is a combiner and when can you use one?", "A mini reducer that runs on each map task's output before the shuffle to shrink it. The operation must be associative and commutative, and its input and output types must equal the map output types. Hadoop may run it zero or more times."),
    ("mapreduce", "What is a partitioner?", "It decides which reducer receives each key. The default HashPartitioner uses hash(key) mod number of reducers."),
    ("mapreduce", "What is a Writable?", "Hadoop's interface for compact binary serialization, with write() and readFields(). All keys and values must be Writable; keys must also be comparable for sorting."),
    ("mapreduce", "What does the mapper receive as input?", "With TextInputFormat, the key is the byte offset of the line (LongWritable) and the value is the line (Text)."),
    ("mapreduce", "What files does a job produce?", "One part-r-NNNNN file per reducer (we have one: part-r-00000) and an empty _SUCCESS marker."),
    ("mapreduce", "Why must the output directory not exist?", "Hadoop refuses to overwrite it, which protects earlier results. We delete it with hdfs dfs -rm -r before re-running."),
    ("mapreduce", "What is data locality?", "Running a map task on the node that stores its block, so code moves to the data instead of data moving across the network."),
    # our code
    ("code", "Walk me through MR1.", "Each mapper keeps the highest total it has seen in an instance field, emits nothing in map(), and in cleanup() writes its single best row under key \"TOP\". The one reducer receives 7 candidates and picks the maximum: Dave Hoff, 1407.5 kg."),
    ("code", "Why does MR1 write in cleanup() instead of map()?", "cleanup() runs once after the whole split is processed, so only then is the split's maximum known. Writing in map() would emit every row."),
    ("code", "Why does MR1 use the key \"TOP\" and one reducer?", "A constant key puts all candidates in one reduce group, and setNumReduceTasks(1) guarantees one reducer, so there is exactly one global answer and one output file."),
    ("code", "Why is there no combiner in MR1?", "The mapper already reduces each split to one record (in-mapper combining), so a combiner would have nothing left to shrink."),
    ("code", "What does split(\",\", -1) do?", "Splits the line on commas and keeps trailing empty strings, so a row whose last columns are empty still produces 42 fields."),
    ("code", "Walk me through MR2.", "The mapper emits (equipment, tuple with min = max = sum = total, count = 1). A combiner merges tuples per key inside each map task. The reducer merges all of them and prints min, max, count and average = sum / count."),
    ("code", "Why a custom Writable in MR2?", "The value must carry four numbers through the shuffle. A Writable class serializes them compactly and gives us a typed merge() method."),
    ("code", "Why store sum and count instead of the average?", "Averages cannot be merged: the average of averages is wrong when groups differ in size. Sums and counts add up exactly, and the average is computed once at the end."),
    ("code", "Why does MR2 need a separate Combiner class?", "Its reducer outputs Text, but a combiner must output the map output type (the tuple). So the reducer cannot double as the combiner."),
    ("code", "Why must write() and readFields() use the same order?", "They are the two halves of one binary format. If the order differs, fields are read into the wrong variables."),
    ("code", "Why copy the first value in the combiner instead of keeping it?", "Hadoop reuses the same object for each value in the iterator, so a stored reference would be overwritten by the next value."),
    ("code", "Walk me through MR3.", "Word count on column 34: the mapper emits (federation, 1), and the reducer sums. The reducer class is also registered as the combiner."),
    ("code", "Why can MR3's reducer be the combiner?", "Summing is associative and commutative, and the reducer's input and output types are both (Text, LongWritable), the map output types."),
    ("code", "Why is MR3's output alphabetical?", "The shuffle sorts by key, so the reducer sees federations in alphabetical order. We sort by count afterwards with sort -k2 -nr."),
    ("code", "What happens to a row where TotalKg is not a number?", "Double.parseDouble throws NumberFormatException, which we catch and ignore, so the row is skipped and the job continues."),
    ("code", "How do you compile and package a job?", "javac -cp \"$(hadoop classpath)\" -d build src/pl/toptotal/*.java, then jar cf TopTotal.jar -C build ., then hadoop jar TopTotal.jar pl.toptotal.TopTotalDriver <input> <output>."),
    # pig
    ("pig", "What is Pig and why use it?", "A high-level dataflow platform on Hadoop. Scripts in Pig Latin are compiled into MapReduce jobs, so questions that need many Java classes take about ten lines."),
    ("pig", "Explain the first three lines of your Pig scripts.", "LOAD reads the CSV from HDFS with PigStorage(','), giving positional fields $0…$41. FILTER drops the header and empty values. FOREACH … GENERATE keeps only the needed columns and casts them to proper types."),
    ("pig", "What is the difference between GROUP ALL and GROUP BY?", "GROUP ALL puts every tuple into one group, for a global result. GROUP BY x makes one group per value of x, for per-category results. That one change turns Pig 2 into Pig 3."),
    ("pig", "What does FLATTEN do?", "It un-nests a bag, turning a bag of 10 tuples into 10 separate output tuples."),
    ("pig", "Why cast $25 to double?", "Without a schema the field is a bytearray, and sorting it as text would put 999 above 1000. As a double, the sort is numeric."),
    ("pig", "Why is ORDER inside a nested FOREACH?", "A top-level ORDER BY failed with Pig 0.17 on Hadoop 3 in our setup, and a nested ORDER plus LIMIT is the standard way to write top-N per group anyway."),
    ("pig", "Where does STORE write the output?", "A relative path goes into the HDFS home directory, e.g. /user/shinzuu/Top10Dots.txt/part-r-00000."),
    ("pig", "When does a Pig script actually run?", "Pig is lazy: statements only build a plan. STORE or DUMP triggers compilation into MapReduce jobs and execution."),
    ("pig", "Why did top5Federations become two jobs?", "It groups twice (by federation to count, then ALL to rank), and Pig compiled it into two MapReduce jobs. So YARN shows 9 applications for 8 analyses."),
    ("pig", "What are local mode and MapReduce mode?", "pig -x local runs in one JVM on local files, good for testing. pig -x mapreduce runs real MapReduce jobs on YARN over HDFS, which is what we used."),
    ("pig", "What do DUMP, DESCRIBE, EXPLAIN and ILLUSTRATE do?", "DUMP prints a relation's data, DESCRIBE its schema, EXPLAIN its execution plans, and ILLUSTRATE a small sample through each step."),
    # results / verification
    ("results", "How do you know your results are correct?", "An awk script recomputed all eight answers directly from the CSV without Hadoop, and every value matched. MR3 and Pig 1 also agree with each other, and in the demo each output is diffed against the saved result."),
    ("results", "What were your main findings?", "Highest total 1407.5 kg by Dave Hoff (Multi-ply). Highest Dots 818.06 by Deana Tollefson. THSPA is the busiest federation with 535,620 entries. Wraps has the highest average total (513.71 kg) and Raw the most entries (1,845,444 with a total)."),
    ("results", "How long did the jobs take?", "About 35–40 seconds per MapReduce job and about 1 minute per Pig script on our laptop, with 7 map tasks each."),
    # what-if
    ("what if", "How would you find the average Dots per sex in MapReduce?", "Mapper: key = f[1] (sex), value = (sum = Dots, count = 1) using a Writable like MinMaxCountAvgTuple, skipping empty f[27]. Combiner merges sums and counts; reducer outputs sum / count."),
    ("what if", "How would you count entries per country in Pig?", "LOAD, FILTER BY $37 != '', FOREACH GENERATE (chararray)$37 AS country, GROUP BY country, FOREACH GENERATE group, COUNT(...), STORE."),
    ("what if", "What would change with 3 reducers in MR3?", "Keys would be hash-partitioned across three reducers, producing part-r-00000 to part-r-00002, each sorted by key on its own. The totals would be the same."),
    ("what if", "What if you set 3 reducers in MR1?", "All records still share key \"TOP\", so one reducer gets all 7 and the other two write empty files. That is why the driver fixes it at 1."),
    ("what if", "How would this scale to a real cluster?", "The code does not change. More DataNodes store the blocks with replication 3, and more NodeManagers run the 7 map tasks in parallel on different machines, close to their data."),
]


def s_viva():
    return ("""
<h2><small>Viva</small>Questions the examiner may ask</h2>
<p>Try to answer out loud before opening each one. Filter by topic.</p>
<div class="filters" id="qa-filters"></div>
""" + "".join(qa(t, q, a) for t, q, a in QA))


MCQ = [
    {"q": "Which command deletes a non-empty HDFS directory?", "o": ["hadoop fs -rmdir /dir1", "hadoop fs -rm /dir1", "hadoop fs -rm -r /dir1", "hadoop fs -del /dir1"], "a": 2, "why": "-rmdir fails on non-empty directories and plain -rm refuses a directory (\"Is a directory\")."},
    {"q": "put is equivalent to…", "o": ["copyToLocal", "copyFromLocal", "moveToLocal", "cat"], "a": 1, "why": "put and copyFromLocal both copy local → HDFS; get and copyToLocal go HDFS → local."},
    {"q": "hadoop fs -mkdir /a/b/c fails when /a/b is missing. The fix is…", "o": ["-mkdir -r", "-mkdir -p", "-mkdir -f", "run it twice"], "a": 1, "why": "-p creates the missing parent directories."},
    {"q": "How many data rows does the dataset have?", "o": ["4,030,220", "4,030,219", "3,759,965", "1,012,540"], "a": 1, "why": "4,030,219 data rows. wc -l prints 4,030,220 because it counts the header too; 3,759,965 is the rows with a TotalKg."},
    {"q": "Which index is TotalKg?", "o": ["$25", "$26", "$27", "$34"], "a": 0, "why": "0-based index 25 (the 26th column). $27 is Dots, $34 is Federation."},
    {"q": "How many map tasks ran for each job, and why?", "o": ["1, one file", "3, replication", "7, one per 128 MB block", "42, one per column"], "a": 2, "why": "785.5 MB / 128 MB = 6.1, so 7 blocks and 7 input splits."},
    {"q": "Which daemon stores HDFS metadata?", "o": ["DataNode", "NameNode", "ResourceManager", "SecondaryNameNode"], "a": 1, "why": "The NameNode holds the namespace and block map; DataNodes hold the data."},
    {"q": "What is our replication factor?", "o": ["0", "1", "2", "3"], "a": 1, "why": "dfs.replication = 1 because there is a single DataNode."},
    {"q": "In MR1, where does the mapper write its output?", "o": ["In map(), once per row", "In setup()", "In cleanup(), once per split", "In the driver"], "a": 2, "why": "cleanup() runs once after the split, when the split's maximum is known."},
    {"q": "How many records reach the MR1 reducer?", "o": ["1", "7", "3,759,965", "4,030,219"], "a": 1, "why": "One best row from each of the 7 mappers."},
    {"q": "Why does MR2 store sum and count rather than the average?", "o": ["It is faster to print", "Averages cannot be merged correctly", "Writable cannot hold doubles", "The report needs sums"], "a": 1, "why": "The average of averages is wrong for groups of different sizes; sums and counts merge exactly."},
    {"q": "Why can't SummarizationReducer be used as MR2's combiner?", "o": ["It is too slow", "Its output value type is Text, not the tuple", "Combiners cannot loop", "It needs two reducers"], "a": 1, "why": "A combiner's output types must equal the map output types (Text, MinMaxCountAvgTuple)."},
    {"q": "Which job reuses its reducer as the combiner?", "o": ["MR1", "MR2", "MR3", "None"], "a": 2, "why": "MR3: summing counts is associative and commutative with matching types."},
    {"q": "Which config property makes MapReduce run on YARN?", "o": ["fs.defaultFS", "dfs.replication", "mapreduce.framework.name", "yarn.nodemanager.aux-services"], "a": 2, "why": "mapreduce.framework.name = yarn in mapred-site.xml."},
    {"q": "What does GROUP lifts ALL produce?", "o": ["One group per row", "One group containing every tuple", "A sorted relation", "An error"], "a": 1, "why": "ALL collects everything into a single bag, for a global top-N."},
    {"q": "What does FLATTEN do in our scripts?", "o": ["Removes duplicates", "Turns a bag of tuples back into separate rows", "Casts types", "Writes to HDFS"], "a": 1, "why": "It un-nests the top-10 bag into 10 output rows."},
    {"q": "Which statement makes a Pig script actually execute?", "o": ["LOAD", "FILTER", "GROUP", "STORE"], "a": 3, "why": "Pig is lazy; STORE (or DUMP) triggers execution."},
    {"q": "How many YARN applications did our 8 analyses create?", "o": ["8", "9", "10", "16"], "a": 1, "why": "top5Federations compiled into 2 MapReduce jobs; the rest were 1 each."},
    {"q": "Who has the highest Dots score?", "o": ["Dave Hoff", "Jenna Odziana", "Deana Tollefson", "Emilio Valle"], "a": 2, "why": "Deana Tollefson, 818.06, and 5 of the top 10 places."},
    {"q": "Which equipment category has the highest average total?", "o": ["Raw", "Multi-ply", "Single-ply", "Wraps"], "a": 3, "why": "Wraps, 513.71 kg."},
    {"q": "What port is the YARN ResourceManager web UI?", "o": ["9000", "8088", "9870", "19888"], "a": 1, "why": "8088. 9870 is the NameNode UI, 19888 JobHistory, 9000 the HDFS RPC address."},
    {"q": "What happens if the output directory already exists?", "o": ["It is overwritten", "Results are appended", "The job fails with FileAlreadyExistsException", "A new name is chosen"], "a": 2, "why": "Hadoop refuses to overwrite output; delete it with hdfs dfs -rm -r first."},
    {"q": "What is the SecondaryNameNode's job?", "o": ["Hot standby for the NameNode", "Checkpointing the edit log into the fsimage", "Storing a second copy of blocks", "Scheduling jobs"], "a": 1, "why": "It checkpoints metadata; it is not a backup NameNode."},
    {"q": "Why is (double)$25 needed before ORDER BY total?", "o": ["To save memory", "So sorting is numeric, not text", "PigStorage requires it", "To skip empty values"], "a": 1, "why": "As text, \"999\" sorts above \"1000\"."},
    {"q": "The mapper input key with TextInputFormat is…", "o": ["the line number", "the byte offset of the line", "the file name", "the first column"], "a": 1, "why": "LongWritable byte offset; the value is the line as Text."},
]

BLANKS = [
    {"s": "Lab 2: copy a local file into HDFS with hadoop fs -___ command3.txt /dir1.", "a": ["copyFromLocal", "put"]},
    {"s": "Lab 2: hadoop fs -___ removes only an empty directory.", "a": ["rmdir"]},
    {"s": "Lab 2: the HDFS web UI is at http://localhost:___.", "a": ["9870"]},
    {"s": "The dataset has ___ columns.", "a": ["42"]},
    {"s": "The default HDFS block size is ___ MB.", "a": ["128"]},
    {"s": "Our CSV is stored in HDFS at /powerlifting/___.", "a": ["openpowerlifting.csv"]},
    {"s": "The HDFS address in core-site.xml is hdfs://localhost:___.", "a": ["9000"]},
    {"s": "The NameNode web UI runs on port ___.", "a": ["9870"]},
    {"s": "The Java version we used is ___.", "a": ["11", "java 11", "openjdk 11"]},
    {"s": "Hadoop version: ___.", "a": ["3.4.1"]},
    {"s": "Pig version: ___.", "a": ["0.17.0", "0.17"]},
    {"s": "The Dots column is at index $___.", "a": ["27"]},
    {"s": "The Federation column is at index $___.", "a": ["34"]},
    {"s": "MR1 emits every candidate under the constant key \"___\".", "a": ["TOP"]},
    {"s": "MR1's reducer receives ___ records.", "a": ["7", "seven"]},
    {"s": "MR2's custom value class is called ___.", "a": ["MinMaxCountAvgTuple"]},
    {"s": "A custom Hadoop value type implements the ___ interface.", "a": ["Writable"]},
    {"s": "The two Writable methods are write() and ___().", "a": ["readFields"]},
    {"s": "The reducer output file is named part-r-___.", "a": ["00000"]},
    {"s": "The command that lists running Java daemons is ___.", "a": ["jps"]},
    {"s": "The busiest federation is ___.", "a": ["THSPA"]},
    {"s": "The highest total ever lifted is ___ kg.", "a": ["1407.5"]},
    {"s": "Pig reads a comma-separated file with USING PigStorage('___').", "a": [","]},
    {"s": "In Pig, GROUP … ___ puts every tuple into a single group.", "a": ["ALL"]},
    {"s": "yarn-site.xml sets aux-services to ___.", "a": ["mapreduce_shuffle"]},
    {"s": "Number of distinct federations: ___.", "a": ["475"]},
    {"s": "Rows with an empty TotalKg: ___.", "a": ["270,254", "270254"]},
]

DRILL = [
    {"task": "Lab 2: make /dir1 and /dir1/newdir in HDFS, then list /dir1.", "cmd": ["hadoop fs -mkdir /dir1", "hadoop fs -mkdir /dir1/newdir", "hadoop fs -ls /dir1"]},
    {"task": "Lab 2: copy command3.txt into /dir1 and show its contents.", "cmd": ["hadoop fs -copyFromLocal command3.txt /dir1", "hadoop fs -cat /dir1/command3.txt"], "note": "Output: command3 - hello from HDFS basics lab"},
    {"task": "Lab 2: upload exampleput.txt into /dir1/newdir with put, then download it with get.", "cmd": ["hadoop fs -put exampleput.txt /dir1/newdir", "mkdir -p downloaded", "hadoop fs -get /dir1/newdir/exampleput.txt downloaded/"]},
    {"task": "Lab 2: copy /dir1/command3.txt out of HDFS with copyToLocal.", "cmd": ["hadoop fs -copyToLocal /dir1/command3.txt downloaded/"]},
    {"task": "Lab 2: delete one file, then an empty directory, then a whole directory tree.", "cmd": ["hadoop fs -rm /dir1/command3.txt", "hadoop fs -rm /dir1/newdir/exampleput.txt", "hadoop fs -rmdir /dir1/newdir", "hadoop fs -rm -r /dir1"]},
    {"task": "Start HDFS, YARN and the history server, then show the daemons.", "cmd": ["start-dfs.sh", "start-yarn.sh", "mapred --daemon start historyserver", "hdfs dfsadmin -safemode wait", "jps"]},
    {"task": "Show what is in HDFS under /powerlifting, with readable sizes.", "cmd": ["hdfs dfs -ls -h /powerlifting"]},
    {"task": "Create /powerlifting in HDFS and upload the CSV to it.", "cmd": ["hdfs dfs -mkdir -p /powerlifting", "hdfs dfs -put openpowerlifting-2026-09-05-b8b9bf6e.csv /powerlifting/openpowerlifting.csv"]},
    {"task": "Show how many blocks the CSV has in HDFS.", "cmd": ["hdfs fsck /powerlifting/openpowerlifting.csv -files -blocks"]},
    {"task": "Compile MR1 and build its jar.", "cmd": ["cd mr/toptotal", "javac -cp \"$(hadoop classpath)\" -d build src/pl/toptotal/*.java", "jar cf TopTotal.jar -C build ."]},
    {"task": "Run MR1 and print its result.", "cmd": ["hadoop jar TopTotal.jar pl.toptotal.TopTotalDriver /powerlifting/openpowerlifting.csv /powerlifting/out_toptotal", "hdfs dfs -cat /powerlifting/out_toptotal/part-r-00000"]},
    {"task": "MR2 failed because the output exists. Fix it and re-run.", "cmd": ["hdfs dfs -rm -r -f /powerlifting/out_summarization", "hadoop jar Summarization.jar pl.summarization.SummarizationDriver /powerlifting/openpowerlifting.csv /powerlifting/out_summarization"]},
    {"task": "Show the top 10 federations from MR3's output, ranked by count.", "cmd": ["hdfs dfs -cat /powerlifting/out_federation/part-r-00000 | sort -t$'\\t' -k2 -nr | head -10"], "note": "Without the sort, the output is alphabetical by federation."},
    {"task": "Run the top-10 Dots Pig script on the cluster and print the result.", "cmd": ["pig -x mapreduce -f top10Dots.pig", "hdfs dfs -cat 'Top10Dots.txt/part-*'"]},
    {"task": "List finished YARN applications.", "cmd": ["yarn application -list -appStates FINISHED"]},
    {"task": "Print the dataset's column names with numbers.", "cmd": ["head -1 openpowerlifting-2026-09-05-b8b9bf6e.csv | tr ',' '\\n' | cat -n"], "note": "cat -n counts from 1, so TotalKg shows as 26 even though its index is 25."},
    {"task": "Stop the whole cluster.", "cmd": ["mapred --daemon stop historyserver", "stop-yarn.sh", "stop-dfs.sh"]},
]


def s_quiz():
    return """
<h2><small>Self-test</small>Quiz</h2>
<p>Click an answer. The correct one turns green and the explanation appears.</p>
<span class="score" id="mcq-score"></span> <button class="btn" id="mcq-reset">reset</button>
<div class="quiz" id="mcq"></div>
<h3>Fill in the blanks</h3>
<p>Type the answer and press Enter or check.</p>
<div class="quiz" id="blanks"></div>
"""


def s_facts():
    return """
<h2><small>Last look</small>Hard facts table</h2>
""" + table(["Thing", "Value"], [
        ["Dataset", "OpenPowerlifting bulk CSV, snapshot 2026-09-05, public domain"],
        ["Size / rows / columns", "785.5 MB (823,619,397 bytes) / 4,030,219 + header / 42"],
        ["Rows with TotalKg / empty", "3,759,965 / 270,254"],
        ["Sex split", "M 2,903,501 · F 1,126,519 · Mx 199"],
        ["Date range", "1964-09-05 to 2026-08-30"],
        ["Federations", "475"],
        ["Software", "Hadoop 3.4.1, Pig 0.17.0, OpenJDK 11, single node (pseudo-distributed)"],
        ["Daemons", "NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager, JobHistoryServer"],
        ["Ports", "9000 HDFS RPC · 9870 NameNode UI · 9868 SecondaryNameNode · 8088 YARN UI · 19888 JobHistory"],
        ["HDFS", "block size 128 MB, 7 blocks, replication 1, path /powerlifting/openpowerlifting.csv"],
        ["MR1 TopTotal", "in-mapper max, key \"TOP\", 1 reducer → Dave Hoff #1, Multi-ply, 2019-10-28, 1407.5 kg"],
        ["MR2 Summarization", "custom Writable (min, max, sum, count) + separate combiner → Wraps avg 513.71, Raw count 1,845,444"],
        ["MR3 Federation", "(federation, 1), reducer = combiner → THSPA 535,620 · USAPL 365,199 · THSWPA 325,029"],
        ["Pig 1", "top 5 federations = MR3 top 5; compiled into 2 jobs"],
        ["Pig 2", "top 10 totals, Dave Hoff 8 of 10"],
        ["Pig 3", "top 10 per equipment (60 rows): Raw 1225 Engelbrecht, Single-ply 1296 Sumner"],
        ["Pig 4", "top 10 Dots: 818.06 Deana Tollefson, 5 of 10"],
        ["Pig 5", "top 10 Dots per sex (30 rows): F 818.06, M 783.48 Dave Hoff, Mx 407.79 Emilio Valle"],
        ["Run times", "MapReduce about 35–40 s each, Pig about 1 min each"],
        ["Verification", "awk ground truth over the CSV; all 8 match; MR3 = Pig 1"],
    ])


def sections():
    return [
        ("start", "Start", s_start()),
        ("journey", "How we did it", s_journey()),
        ("dataset", "Dataset", s_dataset()),
        ("hadoop", "HDFS + YARN", s_hadoop()),
        ("lab2", "Lab 2 HDFS", s_lab2()),
        ("mrtheory", "MapReduce theory", s_mrtheory()),
        ("mr1", "MR1", s_mr1()),
        ("mr2", "MR2", s_mr2()),
        ("mr3", "MR3", s_mr3()),
        ("pigtheory", "Pig theory", s_pigtheory()),
        ("pig", "Pig scripts", s_pig()),
        ("compare", "MR vs Pig", s_compare()),
        ("terminal", "Terminal", s_terminal()),
        ("viva", "Viva Q&A", s_viva()),
        ("quiz", "Quiz", s_quiz()),
        ("facts", "Hard facts", s_facts()),
    ]
