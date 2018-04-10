<?php
header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: *");


$courseUnitCode = null;
$studentNumber = null;
if ($_GET) {
    if ($_GET['courseUnitCode']) {
        $courseUnitCode = $_GET['courseUnitCode'];
    }
    if ($_GET['studentNumber']) {
        $studentNumber = $_GET['studentNumber'];
        if (strlen($studentNumber)==0) {
            $studentNumber = null;
        }
    }
}

$postdata = null;
if ($courseUnitCode && $studentNumber && $_POST) {
    if ($_POST['data']) {
        $postdata = $_POST['data'];
    }
}

///////////////////////////////////////////////////////////

$settings = parse_ini_file('/opt/dfs.ini', true);

$conn = pg_pconnect("
    host=".$settings['database']['host']."
    port=".$settings['database']['port']."
    dbname=".$settings['database']['name']."
    user=".$settings['database']['user']."
    password=".$settings['database']['pass']."
");
if (!$conn) {
    echo "An error occurred.\n";
    exit;
}

$sql0 = '
    INSERT INTO "studentresponse" ("courseUnitCode","studentNumber","timestamp","response")
    VALUES ($1,$2,current_timestamp,$3)
';
if ($postdata) {
    $result0 = pg_query_params($conn,$sql0,array($courseUnitCode,$studentNumber,$postdata));
    if (!$result0) {
        echo "An error occurred.\n";
        exit;
    }
}


$sql1_1 = '
    SELECT "courseUnitCode", "courseUnitName"
    FROM "courseunit"
    WHERE "courseUnitCode"=$1
';
$sql1_2 = '
    SELECT "courseUnitCode", "courseUnitName"
    FROM "courseunit"
';
$sql2 = '
    SELECT "keyConceptOrder", "keyConceptName"
    FROM "keyconcept"
    WHERE "courseUnitCode"=$1
';
$sql3 = '
    SELECT "response"
    FROM "studentresponse"
    WHERE "courseUnitCode"=$1
    AND "studentNumber"=$2
    AND "timestamp" IN (
        select max("timestamp") from "studentresponse" as b
        where b."courseUnitCode"="studentresponse"."courseUnitCode"
        and b."studentNumber"="studentresponse"."studentNumber"
    )
';

$return_arr = array();

if ($courseUnitCode) {
    $result1 = pg_query_params($conn,$sql1_1,array($courseUnitCode));
} else {
    $result1 = pg_query($conn,$sql1_2);
}
if (!$result1) {
    echo "An error occurred.\n";
    exit;
}
while ($courseunit = pg_fetch_assoc($result1)) {
    $studentDataExists=false;
    if ($studentNumber) {
        $result3 = pg_query_params($conn,$sql3,array($courseUnitCode,$studentNumber));
        if (!$result3) {
            echo "An error occurred.\n";
            exit;
        }
        if (pg_num_rows($result3)>0) {
            $studentDataExists=true;
            while ($response = pg_fetch_assoc($result3)) {
                $courseunit = json_decode($response["response"]); //replace!
            }
            array_push($return_arr,$courseunit);
        }
    }
    // no studentNumber given as argument or such data does not exist
    // so return empty template:
    if (!$studentNumber || !$studentDataExists) {
        $result2 = pg_query_params($conn,$sql2,array($courseunit["courseUnitCode"]));
        if (!$result2) {
            echo "An error occurred.\n";
            exit;
        }
        $courseunit["keyConcepts"] = array();
        while ($concept = pg_fetch_assoc($result2)) {
            $concept["disposition"] = array('feeling'=>0, 'significance'=>0, 'mastery'=>0, 'comment'=>'');
            array_push($courseunit["keyConcepts"],$concept);
        }
        array_push($return_arr,$courseunit);
    }// !studentNumber
    //var_dump($courseunit);
}

echo json_encode(
    array(
        "meta"=>array(
            "dataCount"=>pg_num_rows($result1),
            "courseUnitCode"=>$courseUnitCode,
            "studentNumber"=>$studentNumber
        ),
        "data"=>$return_arr
    ),
    JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_NUMERIC_CHECK
);
// end tag missing so that json is not messed up accidentaly
