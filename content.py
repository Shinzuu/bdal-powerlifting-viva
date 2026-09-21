"""Content for the BDAL lab viva guide.

Dense: short theory answers, a command cheat sheet, command drills, and the project in brief.
Commands were all run on this machine; project numbers come from the verified results.
"""

code_block = shell = hbar = None  # injected by build.py

HERO = """
<header class="hero">
  <h1>BDAL lab viva — theory, commands, drills</h1>
  <p>Short answers for the theory questions, every command you may be asked to type, and drills to practise them.
  Project facts at the end.</p>
  <div class="chips">
    <span class="chip">Hadoop 3.4.1 · Pig 0.17.0 · Java 11</span>
    <span class="chip">HDFS · YARN · MapReduce · Pig</span>
    <span class="chip">Command cheat sheet</span>
    <span class="chip">20 drills</span>
  </div>
</header>
"""

ARROW = ('<defs><marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--muted)"/></marker></defs>')


def svg(w, h, inner, cap=None, label="diagram"):
    c = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<div class="figwrap"><svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}">{ARROW}{inner}</svg>{c}</div>'


def box(x, y, w, h, cls, lines):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" class="{cls}"/>']
    n = len(lines)
    for i, ln in enumerate(lines):
        ty = y + h / 2 + (i - (n - 1) / 2) * 16 + 4
        out.append(f'<text x="{x + w/2}" y="{ty:.0f}" text-anchor="middle" class="{"t-b" if i == 0 else "t-s"}">{ln}</text>')
    return "".join(out)


def arrow(x1, y1, x2, y2):
    return f'<path d="M{x1},{y1} L{x2},{y2}" class="ar"/>'


def table(head, rows, num=()):
    th = "".join(f'<th class="{"num" if i in num else ""}">{h}</th>' for i, h in enumerate(head))
    trs = "".join("<tr>" + "".join(f'<td class="{"num" if i in num else ""}">{c}</td>' for i, c in enumerate(r))
                  + "</tr>" for r in rows)
    return f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def qa(tag, q, a):
    return (f'<details class="qa" data-tag="{tag}"><summary>{q}<span class="tag">{tag}</span></summary>'
            f'<div class="a">{a}</div></details>')


# ---------------------------------------------------------------- sections
def s_theory():
    return """
<h2><small>Theory</small>What each piece is, and why it exists</h2>
""" + table(["Term", "What it is", "Why it exists"], [
        ["<b>Hadoop</b>", "framework for storing and processing huge data across many cheap machines", "one machine cannot hold or process terabytes"],
        ["<b>HDFS</b>", "the storage layer: files split into 128 MB blocks, spread over DataNodes", "big files stored across many disks, with copies for safety"],
        ["<b>NameNode</b>", "the master: keeps file names, block list, block locations (metadata only)", "something must know where every block lives"],
        ["<b>DataNode</b>", "the workers: store the actual blocks, send heartbeats", "the real disks"],
        ["<b>SecondaryNameNode</b>", "merges the edit log into the fsimage (checkpoint)", "keeps the edit log from growing forever; <b>not a backup</b>"],
        ["<b>YARN</b>", "the cluster's resource manager and job scheduler", "many jobs share one cluster; something must hand out CPU and memory"],
        ["<b>ResourceManager</b>", "one per cluster: accepts jobs, grants containers", "central scheduler"],
        ["<b>NodeManager</b>", "one per machine: launches and watches containers", "local agent"],
        ["<b>ApplicationMaster</b>", "one per job, runs in a container: asks for containers, tracks tasks", "each job manages itself instead of the RM doing everything"],
        ["<b>Container</b>", "a slice of memory + CPU where one task runs", "isolation and accounting"],
        ["<b>MapReduce</b>", "programming model: map → shuffle &amp; sort → reduce", "lets one program run in parallel over all blocks"],
        ["<b>JobHistoryServer</b>", "keeps logs and counters of finished jobs (port 19888)", "the RM forgets jobs once they finish"],
        ["<b>Pig</b>", "high-level dataflow language (Pig Latin) compiled into MapReduce jobs", "ten lines instead of several Java classes"],
    ]) + svg(860, 300, "".join([
        '<text x="200" y="20" text-anchor="middle" class="t-b">HDFS — storage</text>',
        '<text x="640" y="20" text-anchor="middle" class="t-b">YARN — compute</text>',
        box(20, 35, 360, 62, "bxa", ["NameNode", "metadata: blocks and where they are · UI 9870"]),
        box(20, 110, 175, 62, "bxa", ["DataNode", "stores blocks"]),
        box(205, 110, 175, 62, "bx", ["SecondaryNameNode", "checkpoints · 9868"]),
        box(460, 35, 380, 62, "bxg", ["ResourceManager", "schedules jobs, grants containers · UI 8088"]),
        box(460, 110, 175, 62, "bxg", ["NodeManager", "runs containers"]),
        box(645, 110, 195, 62, "bx", ["JobHistoryServer", "finished jobs · 19888"]),
        arrow(110, 97, 110, 108), arrow(550, 97, 550, 108),
        box(20, 195, 820, 44, "bxw", ["Our cluster: one laptop runs all six daemons (pseudo-distributed)"]),
        box(20, 250, 820, 40, "bxv", ["CSV 785.5 MB → 7 blocks of 128 MB → 7 map tasks · replication 1 · fs.defaultFS = hdfs://localhost:9000"]),
    ]), None, "cluster daemons") + """
<h3>How a MapReduce job runs</h3>
""" + svg(860, 150, "".join([
        box(10, 45, 120, 60, "bxw", ["Input split", "1 per block"]),
        arrow(132, 75, 165, 75),
        box(168, 45, 120, 60, "bxa", ["Map", "(k, v) out"]),
        arrow(290, 75, 323, 75),
        box(326, 45, 130, 60, "bx", ["Combiner", "optional mini-reduce"]),
        arrow(458, 75, 491, 75),
        box(494, 45, 150, 60, "bxv", ["Shuffle + sort", "group by key"]),
        arrow(646, 75, 679, 75),
        box(682, 45, 100, 60, "bxg", ["Reduce", "per key"]),
        arrow(784, 75, 810, 75),
        box(813, 45, 42, 60, "bxw", ["out"]),
    ]), "Output lands in part-r-00000 plus an empty _SUCCESS file.", "mapreduce flow") + """
<ul>
<li><b>Mapper input</b> with TextInputFormat: key = byte offset (LongWritable), value = the line (Text).</li>
<li><b>Combiner</b> allowed when the operation is associative and commutative, and input and output types equal the map output types. It may run zero or many times.</li>
<li><b>Partitioner</b> decides the reducer: default is hash(key) mod number of reducers.</li>
<li><b>Writable</b> is Hadoop's compact serialization; keys must also be comparable so they can be sorted.</li>
<li><b>Output directory must not exist</b>, so a finished result is never overwritten.</li>
<li><b>Data locality</b>: YARN runs a map task on the node holding its block; code moves to the data.</li>
</ul>
<h3>Pig in six lines</h3>
<ul>
<li><code>LOAD … USING PigStorage(',')</code> reads a file; with no schema, fields are <code>$0, $1, …</code></li>
<li><code>FILTER … BY</code> keeps rows · <code>FOREACH … GENERATE</code> picks and casts columns</li>
<li><code>GROUP … ALL</code> = one group (global) · <code>GROUP … BY x</code> = one group per value</li>
<li><code>ORDER … DESC</code>, <code>LIMIT n</code>, <code>FLATTEN(bag)</code> un-nests a bag back into rows</li>
<li><b>Lazy:</b> nothing runs until <code>STORE</code> (to HDFS) or <code>DUMP</code> (to screen)</li>
<li>Modes: <code>pig -x local</code> (local files, one JVM) · <code>pig -x mapreduce</code> (HDFS + YARN, what we used)</li>
</ul>
<div class="box say"><b>MapReduce vs Pig, one line</b>Same engine underneath. MapReduce gives control (combiner,
custom Writable, number of reducers); Pig gives speed of writing — a grouped top-N is one word (<code>ALL</code>
→ <code>BY x</code>) instead of a secondary-sort job.</div>
"""


def s_cheat():
    return """
<h2><small>Cheat sheet</small>Every command, grouped</h2>
<h3>Cluster</h3>
""" + table(["Task", "Command"], [
        ["Load the environment", "<code>source ~/bigdata/hadoop-env.sh</code>"],
        ["Start HDFS / YARN / history", "<code>start-dfs.sh</code> · <code>start-yarn.sh</code> · <code>mapred --daemon start historyserver</code>"],
        ["Wait for safe mode to clear", "<code>hdfs dfsadmin -safemode wait</code>"],
        ["List daemons (expect 6)", "<code>jps</code>"],
        ["Cluster report", "<code>hdfs dfsadmin -report</code>"],
        ["Stop everything", "<code>mapred --daemon stop historyserver</code> · <code>stop-yarn.sh</code> · <code>stop-dfs.sh</code>"],
        ["Version", "<code>hadoop version</code>"],
        ["Web UIs", "NameNode 9870 · YARN 8088 · JobHistory 19888"],
    ]) + """
<h3>HDFS files <span class="t-s">(<code>hadoop fs -…</code> and <code>hdfs dfs -…</code> are the same)</span></h3>
""" + table(["Task", "Command"], [
        ["List", "<code>hadoop fs -ls /</code> · <code>-ls -h /powerlifting</code> · <code>-ls -R /dir1</code>"],
        ["Make a directory", "<code>hadoop fs -mkdir /dir1</code> · parents too: <code>-mkdir -p /a/b/c</code>"],
        ["Local → HDFS", "<code>hadoop fs -copyFromLocal file.txt /dir1</code> · same as <code>-put</code> · overwrite: <code>-put -f</code>"],
        ["HDFS → local", "<code>hadoop fs -copyToLocal /dir1/file.txt .</code> · same as <code>-get</code>"],
        ["Show a file", "<code>hadoop fs -cat /dir1/file.txt</code> · first KB <code>-head</code> · last KB <code>-tail</code>"],
        ["Copy / move inside HDFS", "<code>hadoop fs -cp src dst</code> · <code>hadoop fs -mv src dst</code>"],
        ["Empty file", "<code>hadoop fs -touchz /dir1/empty.txt</code>"],
        ["Sizes", "<code>hadoop fs -du -h /dir1</code> · total <code>-du -s -h</code> · counts <code>-count /dir1</code>"],
        ["Delete file / empty dir / tree", "<code>-rm /f.txt</code> · <code>-rmdir /dir1/newdir</code> · <code>-rm -r /dir1</code>"],
        ["Blocks of a file", "<code>hdfs fsck /powerlifting/openpowerlifting.csv -files -blocks</code>"],
        ["HDFS home directory", "<code>hadoop fs -ls</code> with no path = <code>/user/shinzuu</code>"],
    ]) + """
<h3>MapReduce</h3>
""" + table(["Task", "Command"], [
        ["Compile", "<code>javac -cp \"$(hadoop classpath)\" -d build src/pl/toptotal/*.java</code>"],
        ["Package", "<code>jar cf TopTotal.jar -C build .</code> · check with <code>jar tf TopTotal.jar</code>"],
        ["Run", "<code>hadoop jar TopTotal.jar pl.toptotal.TopTotalDriver &lt;input&gt; &lt;output&gt;</code>"],
        ["See the result", "<code>hadoop fs -cat /powerlifting/out_toptotal/part-r-00000</code>"],
        ["Re-run after a failure", "<code>hadoop fs -rm -r -f &lt;output&gt;</code> first"],
    ]) + """
<h3>Pig</h3>
""" + table(["Task", "Command"], [
        ["Run a script on the cluster", "<code>pig -x mapreduce -f top10Dots.pig</code>"],
        ["Run locally (no HDFS)", "<code>pig -x local -f script.pig</code>"],
        ["Interactive shell", "<code>pig</code> → Grunt; leave with <code>quit;</code>"],
        ["Inside Grunt", "<code>DUMP rel;</code> print · <code>DESCRIBE rel;</code> schema · <code>EXPLAIN rel;</code> plans · <code>ILLUSTRATE rel;</code> sample"],
        ["See Pig output", "<code>hadoop fs -cat 'Top10Dots.txt/part-*'</code> — quote the glob"],
        ["Version", "<code>pig -version</code>"],
    ]) + """
<h3>YARN</h3>
""" + table(["Task", "Command"], [
        ["Running apps", "<code>yarn application -list</code>"],
        ["Finished apps", "<code>yarn application -list -appStates FINISHED</code>"],
        ["Kill a job", "<code>yarn application -kill application_&lt;id&gt;</code>"],
        ["Nodes", "<code>yarn node -list</code>"],
    ]) + """
<h3>Errors you may see</h3>
""" + table(["Message", "Fix"], [
        ["<code>FileAlreadyExistsException</code>", "output dir exists: <code>hadoop fs -rm -r -f &lt;out&gt;</code>, run again"],
        ["<code>Name node is in safe mode</code>", "<code>hdfs dfsadmin -safemode wait</code>"],
        ["stuck at <code>map 0% reduce 0%</code>", "no NodeManager: <code>jps</code>, then <code>start-yarn.sh</code>"],
        ["<code>rmdir: Directory is not empty</code>", "use <code>-rm -r</code>"],
        ["<code>rm: Is a directory</code>", "add <code>-r</code>"],
        ["<code>File exists</code> on copyFromLocal", "use <code>-put -f</code>"],
        ["<code>mkdir: No such file or directory</code>", "parent missing: use <code>-mkdir -p</code>"],
        ["<code>ClassNotFoundException</code>", "wrong main class; check <code>jar tf</code> and use the full package name"],
        ["<code>Connection refused … 9000</code>", "HDFS not running: <code>start-dfs.sh</code>"],
        ["<code>WARN util.NativeCodeLoader</code>", "harmless, ignore"],
    ])


def s_drills():
    return """
<h2><small>Practice</small>Type it, then check</h2>
<p>Cover the answer, write the command, then reveal.</p>
<div class="drill" id="drill"></div>
"""


def s_project():
    return """
<h2><small>Our project</small>The facts they may ask</h2>
""" + table(["Question", "Answer"], [
        ["Dataset", "OpenPowerlifting bulk CSV, snapshot 2026-09-05, public domain"],
        ["Size", "785.5 MB (823,619,397 bytes), 4,030,219 rows + header, 42 columns"],
        ["One row means", "one lifter's result at one competition"],
        ["Columns used", "Name $0 · Sex $1 · Equipment $3 · TotalKg $25 · Dots $27 · Federation $34 · Date $36"],
        ["In HDFS at", "<code>/powerlifting/openpowerlifting.csv</code>, 7 blocks, replication 1"],
        ["Jobs", "3 Java MapReduce + 5 Pig scripts = 8 analyses (9 YARN apps: one Pig script compiles to 2 jobs)"],
        ["Run time", "MapReduce ~35–40 s each · Pig ~1 min each"],
        ["Verification", "an awk script recomputes all 8 answers from the CSV; every one matched, and MR3 = Pig 1"],
    ]) + """
<h3>The three MapReduce jobs</h3>
""" + table(["Job", "What it does", "Pattern", "Result"], [
        ["<b>MR1 TopTotal</b>", "highest TotalKg ever", "each mapper keeps its split's max in a field and emits it in <code>cleanup()</code> under key \"TOP\"; 1 reducer picks the biggest of 7", "1407.5 kg — Dave Hoff, Multi-ply, 2019-10-28"],
        ["<b>MR2 Summarization</b>", "min/max/count/avg TotalKg per equipment", "custom <code>Writable</code> holding min, max, <b>sum and count</b> + a combiner; average computed only at the end", "Wraps highest avg 513.71 · Raw largest 1,845,444"],
        ["<b>MR3 Federation</b>", "entries per federation", "word count: mapper emits (federation, 1); the reducer is also the combiner", "THSPA 535,620 · USAPL 365,199 · THSWPA 325,029"],
    ]) + """
<h3>The five Pig scripts</h3>
""" + table(["Script", "Question", "Key line", "Result"], [
        ["top5Federations", "5 busiest federations", "<code>GROUP feds BY federation</code> + <code>COUNT</code>, then <code>GROUP ALL</code> + ORDER/LIMIT 5", "same top 5 as MR3 (2 MR jobs)"],
        ["top10Total", "10 heaviest totals", "<code>GROUP lifts ALL</code>", "Dave Hoff holds 8 of 10"],
        ["top10TotalByEquipment", "top 10 per equipment", "<code>GROUP lifts BY equipment</code>", "Raw 1225 · Single-ply 1296"],
        ["top10Dots", "10 best Dots", "<code>GROUP lifts ALL</code>", "818.06 Deana Tollefson"],
        ["top10DotsBySex", "top 10 Dots per sex", "<code>GROUP lifts BY sex</code>", "F 818.06 · M 783.48 · Mx 407.79"],
    ]) + """
<div class="box say"><b>Three answers worth memorising</b>Why sum and count, not the average: averages cannot be
merged. Why the MR3 reducer can be the combiner: addition is associative and commutative and the types match.
Why the mapper's max is emitted in <code>cleanup()</code>: only then is the whole split seen, and it cuts the
shuffle from 4 million records to 7.</div>
"""


QA = [
    ("hadoop", "What is Hadoop?", "An open-source framework for storing and processing very large datasets on clusters of ordinary machines: HDFS for storage, YARN for resources, MapReduce as the processing model."),
    ("hadoop", "What is HDFS and how does it store a file?", "The distributed file system. A file is split into blocks (128 MB by default), each block stored on DataNodes and replicated. Our 785.5 MB CSV is 7 blocks with replication 1."),
    ("hadoop", "What does the NameNode hold?", "Metadata only: the directory tree, the file-to-block mapping and block locations. The data itself lives on DataNodes."),
    ("hadoop", "Is the SecondaryNameNode a backup?", "No. It merges the edit log into the fsimage (checkpointing) so restarts are fast and the log stays small."),
    ("hadoop", "What is YARN and why is it needed?", "The resource manager and scheduler. Without it, MapReduce would have to schedule the cluster itself, and only MapReduce could use it. YARN lets many frameworks share one cluster."),
    ("hadoop", "Name the YARN components.", "ResourceManager (one per cluster), NodeManager (one per node), a per-job ApplicationMaster, and containers where tasks run."),
    ("hadoop", "What is replication and why is yours 1?", "The number of copies of each block, normally 3 for fault tolerance. We have one DataNode, so only one copy is possible."),
    ("hadoop", "What is safe mode?", "A read-only state at NameNode start-up while DataNodes report their blocks. Writes and jobs fail until it clears."),
    ("hadoop", "Why does a single-machine Hadoop need SSH?", "The start scripts launch each daemon over SSH, even to localhost."),
    ("hadoop", "Which six daemons should jps show?", "NameNode, DataNode, SecondaryNameNode, ResourceManager, NodeManager, JobHistoryServer."),
    ("hadoop", "Which config file holds what?", "core-site: fs.defaultFS. hdfs-site: replication and the NameNode/DataNode directories. mapred-site: mapreduce.framework.name = yarn. yarn-site: aux-services = mapreduce_shuffle."),
    ("mapreduce", "Explain MapReduce.", "Map processes each record independently and emits key-value pairs; the shuffle groups them by key; reduce processes each key's values into the result."),
    ("mapreduce", "What is the shuffle?", "Copying map output to the reducers, partitioning by key, sorting and grouping. It crosses the network, so it is the expensive phase."),
    ("mapreduce", "What is a combiner and when is it legal?", "A mini reducer on map output before the shuffle. The operation must be associative and commutative, and its input and output types must equal the map output types."),
    ("mapreduce", "Why must the output directory not exist?", "Hadoop refuses to overwrite it, which protects earlier results."),
    ("mapreduce", "What files does a job write?", "part-r-00000 per reducer, plus an empty _SUCCESS marker."),
    ("mapreduce", "What is a Writable?", "Hadoop's compact binary serialization interface (write / readFields). Keys additionally implement WritableComparable so they can be sorted."),
    ("pig", "What is Pig and why use it?", "A dataflow platform: scripts in Pig Latin are compiled into MapReduce jobs, so a question takes about ten lines instead of several Java classes."),
    ("pig", "GROUP ALL vs GROUP BY?", "ALL puts every row in one group for a global answer; BY x makes one group per value, giving a per-category answer."),
    ("pig", "When does a Pig script actually run?", "Only at STORE or DUMP — Pig is lazy and builds a plan first."),
    ("pig", "Why cast a field to double before ORDER?", "Without a schema a field is a bytearray and sorts as text, so \"999\" would rank above \"1000\"."),
    ("commands", "How do you copy a local file into HDFS and check it?", "hadoop fs -copyFromLocal file.txt /dir1 (or -put), then hadoop fs -ls /dir1 and hadoop fs -cat /dir1/file.txt."),
    ("commands", "How do you get a file out of HDFS?", "hadoop fs -copyToLocal /dir1/file.txt downloaded/ (or -get)."),
    ("commands", "Difference between -rm, -rmdir and -rm -r?", "-rm deletes a file, -rmdir only an empty directory, -rm -r a directory with everything inside."),
    ("commands", "How do you run a MapReduce job from source?", "javac -cp \"$(hadoop classpath)\" -d build src/…/*.java, jar cf X.jar -C build ., then hadoop jar X.jar <MainClass> <input> <output>."),
    ("commands", "How do you run a Pig script on the cluster and see its output?", "pig -x mapreduce -f script.pig, then hadoop fs -cat 'Output.txt/part-*'."),
    ("commands", "How do you show that a file is split into blocks?", "hdfs fsck /powerlifting/openpowerlifting.csv -files -blocks — ours reports 7 blocks, six of 134,217,728 bytes and one of 18,313,029."),
    ("project", "Why did you keep sum and count instead of the average in MR2?", "Averages cannot be merged when groups differ in size; sums and counts add exactly, which also makes a combiner safe."),
    ("project", "Why can MR3's reducer also be the combiner?", "Summing is associative and commutative, and its input and output types are both (Text, LongWritable)."),
    ("project", "Why does MR1 write in cleanup()?", "The split's maximum is only known after the last record, and emitting once per split sends 7 records instead of 4 million."),
]


def s_qa():
    return ("""
<h2><small>Viva</small>Short answers</h2>
<div class="filters" id="qa-filters"></div>
""" + "".join(qa(t, q, a) for t, q, a in QA))


MCQ = [
    {"q": "Default HDFS block size:", "o": ["64 MB", "128 MB", "256 MB", "1 GB"], "a": 1, "why": "128 MB in Hadoop 2 and 3; our 785.5 MB file becomes 7 blocks."},
    {"q": "Which daemon stores the block data itself?", "o": ["NameNode", "DataNode", "ResourceManager", "SecondaryNameNode"], "a": 1, "why": "The NameNode keeps only metadata."},
    {"q": "The SecondaryNameNode:", "o": ["takes over if the NameNode dies", "checkpoints the edit log into the fsimage", "stores a second copy of every block", "schedules jobs"], "a": 1, "why": "It is not a standby."},
    {"q": "YARN exists to:", "o": ["store files", "manage cluster resources and schedule jobs", "compile Java", "replace HDFS"], "a": 1, "why": "RM + NM + per-job ApplicationMaster."},
    {"q": "A combiner is legal when the operation is:", "o": ["any operation", "associative and commutative with matching types", "only summing", "only on one reducer"], "a": 1, "why": "It may run zero, one or many times, so the result must not depend on that."},
    {"q": "The default partitioner sends a key to a reducer by:", "o": ["round robin", "hash(key) mod number of reducers", "key length", "input order"], "a": 1, "why": "HashPartitioner."},
    {"q": "With TextInputFormat, the mapper's input key is:", "o": ["the line number", "the byte offset of the line", "the file name", "the first field"], "a": 1, "why": "LongWritable offset, Text value."},
    {"q": "Running a job whose output directory exists gives:", "o": ["overwrite", "append", "FileAlreadyExistsException", "a new folder"], "a": 2, "why": "Delete it with hadoop fs -rm -r first."},
    {"q": "hadoop fs -rmdir fails on a directory that:", "o": ["is empty", "is not empty", "has one file", "was just created"], "a": 1, "why": "\"Directory is not empty\" — use -rm -r."},
    {"q": "put is the same as:", "o": ["get", "copyToLocal", "copyFromLocal", "moveToLocal"], "a": 2, "why": "get = copyToLocal, put = copyFromLocal."},
    {"q": "A Pig script actually executes at:", "o": ["LOAD", "FILTER", "GROUP", "STORE or DUMP"], "a": 3, "why": "Pig is lazy."},
    {"q": "GROUP lifts ALL gives:", "o": ["one group per row", "one group with every row", "an error", "a sorted relation"], "a": 1, "why": "Used for a global top-N."},
    {"q": "Which port is the YARN web UI?", "o": ["9870", "8088", "9000", "19888"], "a": 1, "why": "9870 NameNode, 19888 JobHistory, 9000 HDFS RPC."},
    {"q": "How many map tasks did each of our jobs run?", "o": ["1", "3", "7", "42"], "a": 2, "why": "One per input split, and the CSV is 7 blocks."},
    {"q": "In MR2 the mapper's value is:", "o": ["the whole CSV line", "a tuple of min, max, sum, count", "an average", "an IntWritable"], "a": 1, "why": "A custom Writable; the average is derived at the end."},
]

BLANKS = [
    {"s": "Start HDFS with ___.", "a": ["start-dfs.sh"]},
    {"s": "Start YARN with ___.", "a": ["start-yarn.sh"]},
    {"s": "List the Java daemons with ___.", "a": ["jps"]},
    {"s": "Copy a local file into HDFS: hadoop fs -___ file.txt /dir1.", "a": ["copyFromLocal", "put"]},
    {"s": "Copy a file out of HDFS: hadoop fs -___ /dir1/file.txt .", "a": ["copyToLocal", "get"]},
    {"s": "Delete a directory and its contents: hadoop fs -rm ___ /dir1.", "a": ["-r", "r"]},
    {"s": "Show a file's blocks: hdfs ___ /path -files -blocks.", "a": ["fsck"]},
    {"s": "Run a Pig script on the cluster: pig -x ___ -f script.pig.", "a": ["mapreduce"]},
    {"s": "Compile against the Hadoop jars: javac -cp \"$(___)\" -d build src/*.java", "a": ["hadoop classpath"]},
    {"s": "Run a job: ___ jar TopTotal.jar pl.toptotal.TopTotalDriver in out", "a": ["hadoop"]},
    {"s": "Reducer output file is named part-r-___.", "a": ["00000"]},
    {"s": "The NameNode web UI is on port ___.", "a": ["9870"]},
    {"s": "The YARN web UI is on port ___.", "a": ["8088"]},
    {"s": "Default block size is ___ MB.", "a": ["128"]},
    {"s": "Our replication factor is ___.", "a": ["1"]},
    {"s": "Our CSV is stored at /powerlifting/___.", "a": ["openpowerlifting.csv"]},
    {"s": "Number of map tasks per job: ___.", "a": ["7", "seven"]},
    {"s": "Pig statement that triggers execution: ___.", "a": ["STORE", "DUMP"]},
    {"s": "GROUP lifts ___ puts every row into one group.", "a": ["ALL"]},
    {"s": "The busiest federation in our result is ___.", "a": ["THSPA"]},
]

DRILL = [
    {"task": "Start the whole cluster and prove all six daemons are up.",
     "cmd": ["source ~/bigdata/hadoop-env.sh", "start-dfs.sh", "start-yarn.sh", "mapred --daemon start historyserver", "hdfs dfsadmin -safemode wait", "jps"]},
    {"task": "Create /dir1 and /dir1/newdir in HDFS, then list /dir1.",
     "cmd": ["hadoop fs -mkdir /dir1", "hadoop fs -mkdir /dir1/newdir", "hadoop fs -ls /dir1"]},
    {"task": "Copy a local file command3.txt into /dir1 and print it.",
     "cmd": ["hadoop fs -copyFromLocal command3.txt /dir1", "hadoop fs -cat /dir1/command3.txt"]},
    {"task": "Bring /dir1/command3.txt back to a local folder called downloaded.",
     "cmd": ["mkdir -p downloaded", "hadoop fs -copyToLocal /dir1/command3.txt downloaded/"]},
    {"task": "Upload with put and download with get.",
     "cmd": ["hadoop fs -put exampleput.txt /dir1/newdir", "hadoop fs -get /dir1/newdir/exampleput.txt downloaded/"]},
    {"task": "Delete one file, then an empty directory, then a whole tree.",
     "cmd": ["hadoop fs -rm /dir1/command3.txt", "hadoop fs -rmdir /dir1/newdir", "hadoop fs -rm -r /dir1"]},
    {"task": "Upload a file that is already there, without an error.",
     "cmd": ["hadoop fs -put -f command3.txt /dir1"], "note": "Plain -put or -copyFromLocal would say \"File exists\"."},
    {"task": "Create /a/b/c in one command.",
     "cmd": ["hadoop fs -mkdir -p /a/b/c"], "note": "Without -p: \"No such file or directory\"."},
    {"task": "Put the 785 MB dataset into HDFS and confirm its size.",
     "cmd": ["hadoop fs -mkdir -p /powerlifting", "hadoop fs -put openpowerlifting.csv /powerlifting/", "hadoop fs -ls -h /powerlifting"]},
    {"task": "Show that the CSV is split into blocks.",
     "cmd": ["hdfs fsck /powerlifting/openpowerlifting.csv -files -blocks"], "note": "7 blocks: six of 134,217,728 bytes, one of 18,313,029."},
    {"task": "Compile MR1 from source and build its jar.",
     "cmd": ["cd mr/toptotal", "javac -cp \"$(hadoop classpath)\" -d build src/pl/toptotal/*.java", "jar cf TopTotal.jar -C build ."]},
    {"task": "Run MR1 and show its output.",
     "cmd": ["hadoop jar TopTotal.jar pl.toptotal.TopTotalDriver /powerlifting/openpowerlifting.csv /powerlifting/out_toptotal", "hadoop fs -cat /powerlifting/out_toptotal/part-r-00000"]},
    {"task": "The job failed: output directory already exists. Fix and re-run.",
     "cmd": ["hadoop fs -rm -r -f /powerlifting/out_toptotal", "hadoop jar TopTotal.jar pl.toptotal.TopTotalDriver /powerlifting/openpowerlifting.csv /powerlifting/out_toptotal"]},
    {"task": "Show the top 10 federations from MR3's output, ranked by count.",
     "cmd": ["hadoop fs -cat /powerlifting/out_federation/part-r-00000 | sort -t$'\\t' -k2 -nr | head -10"], "note": "The reducer output is sorted by key, so the ranking is done in the shell."},
    {"task": "Run the Pig script that gives the top 10 Dots, then print the result.",
     "cmd": ["pig -x mapreduce -f top10Dots.pig", "hadoop fs -cat 'Top10Dots.txt/part-*'"], "note": "Quote the glob, or the local shell eats the *."},
    {"task": "Write a Pig script that gives the 5 busiest federations (column $34).",
     "cmd": ["raw   = LOAD '/powerlifting/openpowerlifting.csv' USING PigStorage(',');",
             "clean = FILTER raw BY $0 != 'Name' AND $34 != '';",
             "feds  = FOREACH clean GENERATE (chararray)$34 AS federation;",
             "grp   = GROUP feds BY federation;",
             "cnt   = FOREACH grp GENERATE group AS federation, COUNT(feds) AS c;",
             "allg  = GROUP cnt ALL;",
             "top5  = FOREACH allg { s = ORDER cnt BY c DESC; l = LIMIT s 5; GENERATE FLATTEN(l); };",
             "STORE top5 INTO 'Top5Federations.txt';"]},
    {"task": "Change that script to give the top 10 totals per equipment class instead.",
     "cmd": ["lifts = FOREACH clean GENERATE (chararray)$0 AS name, (chararray)$3 AS eq, (double)$25 AS total;",
             "grp   = GROUP lifts BY eq;      -- ALL would give one global list",
             "top   = FOREACH grp { s = ORDER lifts BY total DESC; l = LIMIT s 10; GENERATE FLATTEN(l); };"]},
    {"task": "List finished YARN applications, then kill a running one.",
     "cmd": ["yarn application -list -appStates FINISHED", "yarn application -kill application_1789420893208_0001"]},
    {"task": "Print the dataset's columns with numbers, and count its rows (local file).",
     "cmd": ["head -1 openpowerlifting.csv | tr ',' '\\n' | cat -n", "wc -l openpowerlifting.csv"], "note": "cat -n counts from 1, so TotalKg shows as 26 while its index is $25."},
    {"task": "Stop the cluster in the right order.",
     "cmd": ["mapred --daemon stop historyserver", "stop-yarn.sh", "stop-dfs.sh", "jps"]},
]


def s_quiz():
    return """
<h2><small>Self-test</small>Quiz</h2>
<span class="score" id="mcq-score"></span> <button class="btn" id="mcq-reset">reset</button>
<div class="quiz" id="mcq"></div>
<h3>Fill in the blanks</h3>
<div class="quiz" id="blanks"></div>
"""


def sections():
    return [
        ("theory", "Theory", s_theory()),
        ("cheat", "Cheat sheet", s_cheat()),
        ("drills", "Command drills", s_drills()),
        ("project", "Our project", s_project()),
        ("qa", "Viva answers", s_qa()),
        ("quiz", "Quiz", s_quiz()),
    ]
