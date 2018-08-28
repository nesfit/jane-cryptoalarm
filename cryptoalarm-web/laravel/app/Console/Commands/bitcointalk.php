<?php

namespace Cryptoalarm\Console\Commands;

use Illuminate\Console\Command;
use Facebook\WebDriver\Exception\WebDriverCurlException;
use Facebook\WebDriver\Exception\TimeOutException;
use Facebook\WebDriver\Remote\RemoteWebDriver;
use Facebook\WebDriver\Remote\DesiredCapabilities;
use Facebook\WebDriver\Chrome\ChromeOptions;
use Facebook\WebDriver\WebDriverExpectedCondition;
use Cryptoalarm\AddressMatcher;
use Cryptoalarm\Setting;
use Cryptoalarm\Coin;
use Cryptoalarm\Identity;

class bitcointalk extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'command:bitcointalk {selenium-standalone : Java JAR package of selenium standalone server} {port=4444}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Crawle bitcointalk.org user profiles and save addresses';
    private $matcher;
    private $webdriver;
    private $port;
    const USLEEP_INTERVAL = 650000;
    const PROFILE_URL = 'https://bitcointalk.org/index.php?action=profile;u=';
    const SOURCE = 'bitcointalk';

    /**
     * Execute the console command.
     *
     * @return mixed
     */
    public function handle()
    {
        $this->port = $this->argument('port');
        $this->startup();
        $this->matcher = new AddressMatcher();
        $bitcointalk_last_id = Setting::findOrFail('bitcointalk_last_id');
        $id = $bitcointalk_last_id->value;
        $max_id = $this->getLastMemberId();

        while($id <= $max_id)
        {
            $source = $this->loadProfile($id);
            $matches = $this->matcher->match_addresses($this->clean($source));

            if($matches) 
            {
                $username = substr($this->webdriver->getTitle(), strlen('View the profile of '));
                foreach($matches as $addr => $coins) 
                {
                    foreach($coins as $coin)
                    {
                        $identity = new Identity();
                        $identity->saveItem([
                            'coin' => $coin,
                            'address' => $addr,
                            'label' => $username,
                            'url' => self::PROFILE_URL . $id,
                            'source' => self::SOURCE,
                        ]);

                        print($id . ";" . $coin . ";" . $addr . PHP_EOL);
                    }
                }
            }

            $id++;
        }

        $bitcointalk_last_id->value = $id;
        $bitcointalk_last_id->save();
        $this->shutdown();
    }

    private function loadProfile($id)
    {
        $source = $this->load(self::PROFILE_URL . $id);
        if(strstr($this->webdriver->getTitle(), "An Error Has Occurred")) 
        {
            print('Profile does not exsits\n');
            return NULL;
        }

        return $source;
    }

    private function load($url)
    {
        while(true)
        {
            try 
            {
                $this->webdriver->get($url);
                usleep(self::USLEEP_INTERVAL);

                if($this->webdriver->getTitle() == 'Bitcoin Forum - Too fast / overloaded (503)') {
                    print(PHP_EOL . 'overloaded ' . $url . PHP_EOL);
                    continue;
                }
                return $this->webdriver->getPageSource();
            } catch (WebDriverCurlException $e) {}
        }
    }

    private function clean($text)
    {
        return strip_tags(str_replace('</', ' </', str_replace('<', ' <', $text)));
    }

    private function getLastMemberId()
    {
        $source = $this->load('https://bitcointalk.org/index.php');
        preg_match('/Latest Member: <b> <a href="https:\/\/bitcointalk\.org\/index\.php\?action=profile;u=([0-9]+)/', $source, $match);
        return $match[1];
    }

    private function startup() 
    {
        $selenium = $this->argument('selenium-standalone');
        $command = [
            'java', '-jar', $selenium, '-role node', '-servlet org.openqa.grid.web.servlet.LifecycleServlet',
            '-registerCycle 0', '-port', $this->port, '-register false',  '>/dev/null 2>&1', '&',
        ];
        exec(join(' ', $command));
        $options = new ChromeOptions();
        $options->addArguments(['--headless', '--disable-gpu']);
        $desiredCapabilities = DesiredCapabilities::chrome();
        $desiredCapabilities->setCapability(ChromeOptions::CAPABILITY, $options);
        $this->webdriver = RemoteWebDriver::create(sprintf('http://localhost:%d/wd/hub', $this->port), $desiredCapabilities);
    }

    private function shutdown()
    {
        $this->webdriver->get(sprintf('http://localhost:%d/extra/LifecycleServlet?action=shutdown', $this->port));
        $this->webdriver->close();
    }

}
